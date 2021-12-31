class AddOffer{
    constructor(){
        if(!window.gogole_maps_script){
            var gogole_maps_script = create('script');
            gogole_maps_script.set('defer','defer');
            gogole_maps_script.set('src','https://maps.googleapis.com/maps/api/js?key=AIzaSyCGPkB5X3MJP8-v16BS3gLOH1OflTzpXa4&libraries=places&callback=initMap&type=(cities)');
            gogole_maps_script.set('type','text/javascript');
            gogole_maps_script.onload = function(){
                initMap();
            };
            $('body').append(gogole_maps_script);
        }else{
            initMap();
        }
        $('#submit').on('click',this.save.bind(this));

        var categories = new Menu({
            container: $('#categories'),
            delay: 0,
            toggleButton: $('#toggleCategories'),
            left: 0,
            choice:function(event){
                if(event.target.tagName == 'SPAN'){
                    event.target.parent().click();
                    return;
                }
                $('#id_category').value = event.target.get('categoryId');
                $('.dvm-add-offer-category').text(event.target.text);
                this.close();

                event.stopPropagation();
                event.preventDefault();
                return false;
            }
        });
    }
    save(event){
        http.action = function(){
            if(http.json && http.json.result){
                var offerId = http.json.offerId;
                gallery.objectId = offerId;

                var images = $('#images input[type="file"]');
                var current = 0;
                var last = images.length - 1;

                http.action = function(){
                    current++;
                    if(current == last){
                        http.action = function(){
                            location.href = '/offer/' + offerId;
                        };
                    }
                    if(!images[current])
                        location.href = `/offer/${offerId}`;
                    http.post(`/add/image/${gallery.model}/${gallery.objectId}`,{image:images[current].get('base64')});
                };
                http.post(`/add/image/${gallery.model}/${gallery.objectId}`,{image:images[current].get('base64')});
            }
            else{
                log(http.json.errors);
            }
        };
        http.post('/add/offer',$('#form').serializeJSON());
    }
}

var rules = {
    'name':{
        'required': true,
        'rules':{
            'regex':/[а-яА-Яa-zA-Z0-9\-\_\.]/,
        },
        'errors':{
            'regex':'Неправильный ввод',
        }
    },
    'price':{
        'required': true,
        'rules':{
            'regex':/[0-9]+/,
        },
        'errors':{
            'regex':'Неправильный ввод'
        }
    },
    'description':{
        'required': true,
        'rules':{
            'max_length':1000,
        },
        'errors':{
            'max_length':'Максимальная длина 1000 символов',
        }
    },
    'location_text':{
        'required': true,
        'rules':{
            'regex':/[а-яА-Яa-zA-Z0-9\-\_\.,]/,
        },
        'errors':{
            'regex':'Неправильный ввод',
        }
    }
};