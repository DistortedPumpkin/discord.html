import { AbstractAction } from "./AbstractAction";
import { SendMessageAction } from "./SendMessageAction";

export class ActionManager {

    private static _actions: object;

    constructor() {
        ActionManager._actions = {};
        ActionManager.registerAction(SendMessageAction);
    }

    static getActionClass(actionName: string): any {
        return ActionManager._actions[actionName];
    }

    static getAction(actionName: string, data: cheerio.Cheerio): AbstractAction {
        const actionClass = ActionManager.getActionClass(actionName);
        if (!actionClass) return undefined;
        return new actionClass(data);
    }

    static registerAction(actionType: any) {
        ActionManager._actions[new actionType().actionType] = actionType;
    }

}