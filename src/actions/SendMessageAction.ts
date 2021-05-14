import { HTMLBot } from "../bot";
import { AbstractAction } from "./AbstractAction";

export class SendMessageAction extends AbstractAction {

    data: object;

    constructor(data: cheerio.Cheerio) {
        super("sendMessage");
        if (!data) return;
        this.data = {};
        this.data["content"] = data.html().trim();
    }

    async execute(bot: HTMLBot, context: any): Promise<any> {
        const channelID = this.data["channel"] || context["channel"];
        return await bot.eris.createMessage(channelID, this.data["content"]);
    }
}