import { HTMLBot } from "./bot";
import * as cheerio from 'cheerio';

export class Parser {

    constructor() { }

    parse(bot: HTMLBot, html: string) {
        let parsed = cheerio.load(html)
        parsed('data').each((i, data) => {
  
        const stuff = `${data.attribs.name}: ${x(data).text()} `

        console.log(stuff)
        })
    }

}

