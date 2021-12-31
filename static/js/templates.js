var templates = {
    message: function(message){
        var msgClass = message.owner == userId ? 'from' : 'to';
        return `<div class="message ${msgClass}">
                    <div class="text">${message.text}</div>
                </div>`;
    }
};