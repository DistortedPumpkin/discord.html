import { HTMLBot } from "./bot";
import * as cheerio from 'cheerio';

export class Parser {

    constructor() { }

    parse(bot: HTMLBot, html: string) {

    }

}

let x = cheerio.load(`
<head>
    <data name="token">TOKEN HERE</data>
    <data name="prefix">!</data>
    <data name="status">Running on HTML!</data>
</head>`)
x('data').each((i, data) => {
  
  const stuff = `${data.attribs.name}: ${x(data).text()} `

  console.log(stuff)
})



