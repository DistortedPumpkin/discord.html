import { HTMLBot } from "../bot";

export abstract class AbstractAction {
    readonly actionType: string;
    abstract execute(bot: HTMLBot, context: any): any | Promise<any>;
    constructor(actionType: string) {
        this.actionType = actionType;
    }
}