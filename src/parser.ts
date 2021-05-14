import { load } from "cheerio";
import { ActionManager } from "./actions/ActionManager";
import { HTMLBot } from "./bot";
import { Command } from "./command";
import { Util } from "./util";

export class Parser {

  constructor() { }

  parse(bot: HTMLBot, html: string) {
    const parsed = load(html);

    // Loop over constants in header
    parsed('header > data').each((i, data: any) => {
      bot.globalStorage.set(data.attribs.name, parsed(data).text())
    });

    parsed('div[type=command]').each((i, data) => {
      const cmd_parse = parsed(data);
      const command = new Command(Util.getData(cmd_parse, "name"));
      cmd_parse.find('div[type=code] > div[type=action]')
        .each((i, action_data: any) => {
          const x = parsed(action_data);
          const action = ActionManager.getAction(x.attr("action"), x);
          if (action)
            command.addAction(action);
        });
      bot.addCommand(command);
    });
  }
}

