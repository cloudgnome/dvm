class Auction{
    constructor(){
        if(!window.gogole_maps_script){
            var gogole_maps_script = create('script');
            gogole_maps_script.set('defer','defer');
            gogole_maps_script.set('src','https://maps.googleapis.com/maps/api/js?key=AIzaSyCGPkB5X3MJP8-v16BS3gLOH1OflTzpXa4&libraries=places&callback=initMap');
            gogole_maps_script.set('type','text/javascript');
            gogole_maps_script.onload = function(){
                initMap();
            };
            $('body').append(gogole_maps_script);
        }else{
            initMap();
        }
        var bullets = '';
        var images = $('#slider img');
        for(var i=0;i < images.length;i++){
            bullets += `<button class="glide__bullet" data-glide-dir="=${i}"></button>`;
        }
        $('#carouselSlider').after('<div class="glide__bullets" data-glide-el="controls[nav]"></div>');
        $('.glide__bullets').html(bullets);
        if(this.glide)
            this.glide.destroy();
        this.glide = new Glide('.glide',{type: 'carousel'}).mount();

        $('#slider .prev').on('click touch',function(){view.glide.go('<')});
        $('#slider .next').on('click touch',function(){view.glide.go('>')});
        $('#sendMessage').on('click touch',this.sendMessage);
    }
    sendMessage(){
        var text = $('#chat input')[0].value;
        if(!text)
            return;

        http.action = function(){
            if(http.json && http.json.result){
                location.href = '/chat/' + http.json.chatId;
            }else{
                log(http.json);
            }
        };
        http.post('/chat/send/' + this.get('recieverId'),{'text':text});
    }
}
var view = new Auction();