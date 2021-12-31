class Panel{
    constructor(){
        this.findPath();
        if(this.path.menu)
            this.switchActive(this,$(`a[href="${this.path.menu}"]`)[0]);
    }
    findPath(path){
        if(!path)
            path = location.pathname;
        for(let [pattern,value] of Object.entries(urlpatterns)){
            var regex = new RegExp(pattern);
            if(regex.test(path)){
                this.path = value;
                break;
            }
        }
        if(!this.path)
            this.path = "No pattern matches this url " + path;
    }
    switchActive(panel,elem){
        if(!elem)
            return;
        if(panel.active)
            panel.active.removeClass('active');
        panel.active = elem.parent();
        panel.active.addClass('active');
    }
}

var panel = new Panel();