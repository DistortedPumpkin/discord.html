export class Util {

    constructor() { }

    static getData(parsed: cheerio.Cheerio, name: string): string {
        return parsed.find(`data[name=${name}]`).text();
    }

}