class Messages{
    constructor(messages){
        this.window = $('#text');
        for(var item of messages){
            this.window.after(templates.message(item));
        }
    }
}

var view = new Messages(messages);