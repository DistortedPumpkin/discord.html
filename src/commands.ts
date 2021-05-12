class Command{
  readonly name: string;
  actions: Action[];
  constructor(name: string){
    this.name = name;
    actions = [];
  }
  addAction(action: Action) {
    this.actions.push(action);
  }
}

abstract class Action {
    readonly actionType: string;
    abstract execute(): void;
    constructor(actionType: string){
      this.actionType = actionType;
    }
}

class SendMessageAction extends Action {

  constructor(data: any){
    super("sendMessage");
  }
  
  async execute(bot: HTMLBot, context: any, data: any): Promise<void> {
      const channelID = data["channel"] || context["channel"];
      return bot.createMessage(channelID, {content: data["content"]});
  }  
}
