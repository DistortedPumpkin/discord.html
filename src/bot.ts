import { readFile } from "fs/promises";
import { Parser } from "./parser";
import { Command } from "./commands"

export class HTMLBot {

    globalStorage: Map<string, any>;
    commands: Map<string, Command>;

    private _parser: Parser;

    constructor() {
        this._parser = new Parser();
        this.commands = new Map();
        this.globalStorage = new Map();
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
    
    addCommand(data: any) {
        cmd = Command(data['name'], data['actions'])
        this.commands.set(data.name, cmd)
    }
}
