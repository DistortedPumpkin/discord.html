import { load } from "cheerio";
import { HTMLBot } from "./bot";

export class Parser {

  constructor() { }

  parse(bot: HTMLBot, html: string) {
    const parsed = load(html);

    // Loop over constants in header
    parsed('header > data').each((i, data: any) => {
      bot.globalStorage.set(data.attribs.name,parsed(data).text())
    });
    
    parsed('div[type=command]').each((i, data) => {
      const cmd_data = {};
      const cmd_parse = parsed(data);
      cmd_parse.find('data').each((i, d_data) => {
        cmd_data[d_data.attribs.name] = parsed(d_data).text();
      });
      bot.add_command(cmd_data);
      // bot.commands.set(cmd_data['name'], cmd_data);
    });

  
  }

}

