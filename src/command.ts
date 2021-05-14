import { Message } from "eris";
import { AbstractAction } from "./actions/AbstractAction";
import { HTMLBot } from "./bot";

export class Command {
  readonly name: string;

  actions: AbstractAction[];

  constructor(name: string, actions?: AbstractAction[]) {
    this.name = name;
    this.actions = actions || [];
  }

  addAction(action: AbstractAction) {
    this.actions.push(action);
  }

  async execute(bot: HTMLBot, commandContext: any): Promise<void> {
    for (const action of this.actions) {
      await action.execute(bot, commandContext);
    }
  }

  static getCommandContext(message: Message): any {
    const context = {};
    context["content"] = message.content;
    context["author"] = message.author;
    context["channel"] = message.channel.id;
    context["guild"] = message.guildID;
    return context;
  }
}




