import { readFile } from "fs/promises";
import { Parser } from "./parser";

export class HTMLBot {

    globalStorage: Map<string, any>;

    private _parser: Parser;

    constructor() {
        this._parser = new Parser();
        this.globalStorage.set("prefix", "!");
        this.globalStorage.set("status", "Running on HTML!");
    }

    async addFile(path: string) {
        const html = (await readFile(path)).toString();
        return this.addHTML(html);
    }

    addHTML(html: string) {
        this._parser.parse(this, html);
    }
}