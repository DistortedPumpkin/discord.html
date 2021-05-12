import { load } from "cheerio";
import { HTMLBot } from "./bot";
import { Action } from "./commands"

export class Parser {

  constructor() { }

  parse(bot: HTMLBot, html: string) {
    const parsed = load(html);

    // Loop over constants in header
    parsed('header > data').each((i, data: any) => {
      bot.globalStorage.set(data.attribs.name, parsed(data).text())
    });
    
    parsed('div[type=command]').each((i, data) => {
      const cmd_data = {};
      const cmd_parse = parsed(data);
      const parsed_name = cmd_parse.find('data[name=name]').text();
      cmd_data['name'] = parsed_name;
      const actions = [];
      cmd_parse.find('div[type=code] > div[type=action]').each((i, action_data: any) => {
        actions.push(Action(action_data.attribs.action));
      });
      cmd_data['actions'] = actions;
      bot.addCommand(cmd_data);
    });

  
  }

}

