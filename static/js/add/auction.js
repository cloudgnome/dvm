class AddAuction{
    constructor(){
        this.initMap();
        this.initCategories();
        this.datepicker();
        $('#submit').on('click',this.save);
    }
    datepicker(){
        var test = create('input');
        test.type = 'date';

        if(test.type === 'text') {
            var datepickerCSS = create('link');
            datepickerCSS.set('href','/static/css/datepicker.css');
            datepickerCSS.set('rel','stylesheet');
            datepickerCSS.onload = function(){
                var datepickerJS = create('script');
                datepickerJS.set('src','/static/js/datepicker.js');
                datepickerJS.set('type','text/javascript');
                datepickerJS.onload = function(){
                    var endDatepicker = new TheDatepicker.Datepicker($('#id_end_date'));
                    endDatepicker.options.setInputFormat('Y-n-j');
                    endDatepicker.render();
                };
                $('body').append(datepickerJS);
            };

            $('body').append(datepickerCSS);
        }
    }
    save(event){
        http.action = function(){
            if(http.json && http.json.result){
                var auctionId = http.json.auctionId;
                gallery.objectId = auctionId;

                var images = $('#images input[type="file"]');
                var current = 0;
                var last = images.length - 1;

                http.action = function(){
                    current++;
                    if(current == last){
                        http.action = function(){
                            location.href = '/auction/' + auctionId;
                        };
                    }
                    if(!images[current])
                        location.href = `/offer/${auctionId}`;
                    http.post(`/add/image/${gallery.model}/${gallery.objectId}`,{image:images[current].get('base64')});
                };
                http.post(`/add/image/${gallery.model}/${gallery.objectId}`,{image:images[current].get('base64')});
            }
            else{
                log(http.json.errors);
            }
        };
        http.post('/add/auction',$('#form').serializeJSON());
    }
    initMap(){
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
    }
    initCategories(){
        this.categories = new Menu({
            container: $('#categories'),
            delay: 0,
            toggleButton: $('#toggleCategories'),
            left: 0,
            choice:function(event){
                $('#id_category').value = event.target.get('categoryId');
                $('.dvm-add-offer-category').text(event.target.text);
                this.close();

                event.stopPropagation();
                event.preventDefault();
                return false;
            }
        });
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
    'start_price':{
        'required': true,
        'rules':{
            'regex':/[0-9]+/,
        },
        'errors':{
            'regex':'Неправильный ввод'
        }
    },
    'buyout':{
        'required': true,
        'rules':{
            'regex':/[0-9]+/,
        },
        'errors':{
            'regex':'Неправильный ввод'
        }
    },
    'bid_step':{
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

var validator = new Validator($('#form'),rules);
var view = new AddAuction();
var gallery = new Gallery(model='Auction');