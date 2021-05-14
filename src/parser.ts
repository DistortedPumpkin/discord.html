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
      const cmdParse = parsed(data);
      const command = new Command(Util.getData(cmdParse, "name"));
      cmdParse.find('div[type=code] > div[type=action]')
        .each((i, actionData: any) => {
          const actionParse = parsed(actionData);
          const action = ActionManager.getAction(actionParse.attr("action"), actionParse);
          if (action)
            command.addAction(action);
        });
      bot.addCommand(command);
    });
  }
}

