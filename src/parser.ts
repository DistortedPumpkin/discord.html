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
  
  }

}

