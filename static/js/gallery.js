class Gallery{
    constructor(model,images){
        this.model = model;
        this.clickListener = this.add.bind(this);
        $('#gallery .plus').on('click touch',this.clickListener);
        $('#gallery .remove').on('click touch',this.remove);
        this.images = $('#images');
    }
    add(event){
        var container = event.target;
        var input = create('input');
        input.set('type','file');
        input.hide();
        input.container = container;
        this.input = input;
        this.images.before(input);
        input.on('change',this.render);
        input.click();
        container.parent().removeEvent('click touch',this.add);
    }
    render(){
        var file = this.files[0];
        var reader = new FileReader();
        var input = this;
        reader.onload = function(e){
            var div = input.container;
            div.html('<div class="remove"><i class="fal fa-times"></i></div>');
            div.find('.remove')[0].on('click',gallery.remove);
            input.set('base64',e.target.result);
            var image = create('img');
            image.on('click',gallery.add);
            gallery.input.set('name','images');
            gallery.input.set('value',e.target.result);
            gallery.save(div,image,e.target.result);
        };
        reader.readAsDataURL(file);
    }
    save(div,image,base64){
        image.src = base64;
        div.append(image);
    }
    uploadImage(base64){
        http.post(`/add/image/${this.model}/${this.objectId}`,{image:base64});
    }
    remove(event){
        this.next().remove();
        this.remove();
        event.stopPropagation();
        return false
    }
    removeEvent(item){
        item.removeEvent('click touch',this.clickListener);
    }
}
class GalleryEdit extends Gallery{
    constructor(model,images){
        super(model);
        if(images)
            this.populate(images);
        $('#gallery .remove').on('click touch',this.remove);
    }
    populate(images){
        for(var i=0; i < images.length; i++){
            var item = $('.plus.img-' + (i+1));
            item.html(`
                <div class="remove" item-id="${images[i].id}"><i class="fal fa-times"></i></div>
                <img src="${images[i].image}" alt="" />
            `);
            item.removeClass('plus');
        }
    }
    remove(event){
        var parent = event.target.parent();
        if(event.target.tagName == 'I'){
            parent.click();
            return;
        }
        var agree = confirm('Удалить картину?');
        if(this.get('item-id') && agree){
            http.action = function(){
                if(http.json && http.json.result){
                    parent.clear();
                    parent.on('click touch',gallery.add.bind(gallery));
                }
            };
            http.get(`/remove/image/${gallery.model}/${this.get('item-id')}`);
        }
        event.stopPropagation();
        return false
    }
}