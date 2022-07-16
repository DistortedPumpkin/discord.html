import re
from bs4 import BeautifulSoup, Tag
from discord import Embed
from .errors import CommandMissingData, CommandActionMissingData, CommandActionMissingType
from .commands import Command, Context, Parameter
from .utils import MISSING, to_bool

VAR_PATTERN_1 = re.compile(r'<var context="(local|global)">(.*?)<\/var>')  # noqa
VAR_PATTERN_2 = re.compile(r'(\{\{|\[\[)(.*?)(\}\}|\]\])')  # noqa


class Parser:
    def __init__(self, bot):
        self.bot = bot
    
    def parse(self, html: str, is_main_file: bool = False):
        soup = BeautifulSoup(html, 'html.parser').find('html', recursive=False)

        if is_main_file:
            # Iterate through header vars and add them to storage
            header = soup.find('header', recursive=False)
            if header:
                for data in header.find_all('data', recursive=False):
                    self.bot.storage[data.attrs['name']] = data.attrs['value']
        
        # Iterate through command divs, parse them, and add them to the bot's command mapping
        for div in soup.find_all('div', {'type': 'command'}, recursive=False):
            self.parse_command(div)
    
    def parse_command(self, tag: Tag):
        attrs = {}
        for data in tag.find_all('data', recursive=False):
            key = data.attrs['name']
            attrs[key] = attrs.get(key, []) + [data.attrs['value']]
        if not attrs.get('name'):
            raise CommandMissingData(str(tag), 'name')
        name = attrs['name'][0]
        params = []
        for param_tag in tag.find_all('data', {'type': 'param'}, recursive=False):
            params.append(Parameter(
                param_tag.attrs['name'], 
                param_tag.attrs.get('value') or MISSING,  # Empty string will return MISSING 
                to_bool(param_tag.attrs.get('consume', False))
            ))
        code = tag.find('div', {'type': 'code'}, recursive=False)
        command = Command(name, aliases=attrs['name'][1:], params=params)
        if code:
            for action_tag in code.find_all('div', {'type': 'action'}, recursive=False):
                action = self.bot.action_classes.get(action_tag.attrs.pop('action', '').lower())
                if not action:
                    raise CommandActionMissingType(action_tag)
                contents = action_tag.decode_contents()
                if not contents:
                    raise CommandActionMissingData(action_tag)

                del action_tag.attrs['type']

                data = {
                    'content': self.transform_var(contents),
                    **action_tag.attrs
                }
                command.add_action(action(data))
        self.bot.add_command(command)

    @staticmethod
    def transform_var(tag: str):  # This exists so we don't have to re-parse the variable call every time
        """Transform a <var> tag into a string that's easier to parse
        Example:
            >>> Parser.transform_var('<var context="local">role</var>')
            {{role}}
            >>> Parser.transform_var('<var context="global">role.name</var>')
            [[role]]
        """
        o = lambda g: '{{' if g == 'local' else '[['
        c = lambda g: '}}' if g == 'local' else ']]'

        def repl(m):
            g1 = m.group(1)
            return f"{o(g1)}{m.group(2)}{c(g1)}"
        return VAR_PATTERN_1.sub(repl, tag)

    @staticmethod
    def parse_content_with_variables(content: str, ctx: Context):
        """Parses the variable patterns and returns those variables values, getting them from either local/global storage"""
        def repl(m):
            thing = m.group(2).split('.')
            storage = ctx.storage if m.group(1) == '{{' else ctx.bot.storage
            current = storage.get(thing[0], thing[0])
            if len(thing) < 2:
                return str(current)
            for attr in thing[1:]:  # Deal wiith x.y.z because that must be done after getting the variable from storage
                try:
                    res = getattr(current, attr)
                except AttributeError:
                    return '[undefined]'
                current = res
            return str(current)
        return VAR_PATTERN_2.sub(repl, content)
    
    def parse_for_embed(self, tag: str, ctx: Context) -> Embed:
        """Parse an embed div tag into a discord.Embed object that can be sent on Discord
        Example:
            >>> self.parse_for_embed('''
            ... <div type="embed" title="Hello There" color="#00BEEF">
            ...    <data name="description" value=""> <!-- Add blank value because we want to use variables but value is required for data tags-->
            ...        Hello <var context="local">ctx.author.mention</var>!
            ...    </data>
            ... </div>'''
            ... )
            <discord.Embed object at 0x...>
        """
        tag = BeautifulSoup(tag, 'html.parser').find('div')
        if not tag or tag.attrs.get('type') != 'embed':
            return None

        def get_attribute(t: Tag, attr: str, search_inside=True):
            if t.attrs.get(attr):
                return t.attrs[attr]
            if search_inside:
                if (elem := t.find('data', {'name': attr}, recursive=False)):
                    return elem.attrs.get('value') or self.parse_content_with_variables(self.transform_var(elem.decode_contents()), ctx)
            return None
        
        color = get_attribute(tag, 'color')
        color = int(color[1:], base=16) if color else None
        embed = Embed(title=get_attribute(tag, 'title'), description=get_attribute(tag, 'description'), color=color)
        for field_tag in tag.find_all('fieldset', recursive=False):
            d = {}
            for label in field_tag.find_all('label', recursive=False):
                l_for = label.attrs['for']
                value = label.decode_contents()
                d[l_for] = self.parse_content_with_variables(
                    self.transform_var(str(value)), ctx
                ) if l_for in ('name', 'value') else str(value)
            embed.add_field(
                name=d.get('name'), value=d.get('value'), inline=to_bool(d.get('inline', True))
            )
        
        return embed
        
