class Menu{
    constructor(parameters){
        this.container = parameters.container;
        this.parameters = parameters;
        this.title = this.container.find('span')[0];
        this.prevButton = this.container.find('#prev');
        this.left = parameters.left ? parameters.left : 0;
        this.root = this.container.find('ul')[0];
        this.choice = parameters.choice;

        this.parameters.toggleButton.on('click touch',this.show.bind(this));
        this.container.find('li.branch').on('click touch',this.next.bind(this));
        this.prevButton.on('click touch',this.previous.bind(this));
        this.container.find('.choice').on('click',this.choice.bind(this));
        /*if(this.container.styles('width').includes('%')){
            this.containerWidth = window.width * (parseInt(this.container.styles('width'))/10);
        }else{
            this.containerWidth = parseInt(this.container.styles('width'));
        }*/
    }
    show(event){
        if(this.active){
            this.active.removeClass('open');
            this.active = this.container.find('ul')[0].addClass('open');
        }
        this.container.css('left',`-${this.containerWidth + this.left}px`);
        this.container.show();

        var that = this;
        setTimeout(function(){
            that.container.css('left',`${that.left}px`);
        },this.parameters.delay ? this.parameters.delay : 0);
    }
    next(event){
        if(event.target.tagName == 'SPAN'){
            event.target.parent().click();
            return;
        }
        this.active = event.target.find('ul')[0];

        var that = this;
        setTimeout(function(){
            that.active.addClass('open');
        },this.parameters.delay ? this.parameters.delay : 0);

        this.title.text(event.target.find('span')[0].text());
        this.prevButton.show();

        event.stopPropagation();
        event.preventDefault();
        return false;
    }
    previous(event){
        if(this.active == this.root)
            return;

        this.active.removeClass('open');
        this.active = this.active.parent().parent();
        this.title.text(this.active.parent().find('span')[0].text());

        var that = this;
        setTimeout(function(){
            that.active.addClass('open');
        },this.parameters.delay ? this.parameters.delay : 0);

        if(this.active == this.root){
            this.prevButton.hide();
            this.title.text('Chose a Category');
            return;
        }

        event.stopPropagation();
        event.preventDefault();
        return false;
    }
    close(){
        this.container.hide();
    }
}

var menu = new Menu({
    container: $('#nav'),
    delay: 0,
    toggleButton: $('#toggleMenu'),
    left: 0,
    choice:function(event){
        if(event.target.tagName == 'SPAN'){
            event.target.parent().click();
            return;
        }
        location.href = `/category/${view.model}/${event.target.get('categoryId')}`;
        event.stopPropagation();
        event.preventDefault();
        return false;
    }
});