import { readFile } from "fs/promises";
import { Parser } from "./parser";
import { Command } from "./command"
import { Client, Message } from "eris";
import { ActionManager } from "./actions/ActionManager";

export class HTMLBot {

    globalStorage: Map<string, any>;
    commands: Map<string, Command>;

    private _parser: Parser;

    eris: Client;

    constructor() {
        /*
            Deal with all html
        */
        this._parser = new Parser();
        this.commands = new Map();
        this.globalStorage = new Map();
        this.globalStorage.set("prefix", "!");
        this.globalStorage.set("status", "Running on HTML!");

        /*
            Initialize static helpers
        */
        new ActionManager();
    }

    async addFile(path: string) {
        const html = (await readFile(path)).toString();
        return this.addHTML(html);
    }

    addHTML(html: string) {
        return this._parser.parse(this, html);
    }

    addCommand(command: Command) {
        this.commands.set(command.name, command)
    }

    setupEris() {
        if (!this.globalStorage.has("token")) throw Error("No token found but tried to setup eris");

        this.eris = new Client(this.globalStorage.get("token"));

        this.eris.on("messageCreate", (message: Message) => {
            if (message.author.bot) return;
            if (!message.content.startsWith(this.globalStorage.get("prefix"))) return;
            const commandName = message.content.slice(this.globalStorage.get("prefix").length).split(" ")[0];
            if (!this.commands.has(commandName)) return;
            const context = Command.getCommandContext(message);
            this.commands.get(commandName).execute(this, context);
        });

        return this.eris.connect();

    }
}
