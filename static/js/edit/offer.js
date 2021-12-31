class EditOffer extends AddOffer{
    constructor(id){
        super();
        this.id = id;
    }
    save(event){
        http.action = function(){
            if(http.json && http.json.result){
                var objectId = http.json.objectId;
                gallery.objectId = objectId;

                var images = $('#images input[type="file"]');
                var current = 0;
                var last = images.length - 1;

                if(!images[current]){
                    location.href = `/offer/${objectId}`;
                    return;
                }
                http.action = function(){
                    current++;
                    if(current == last){
                        http.action = function(){
                            location.href = `/offer/${objectId}`;
                        };
                    }
                    if(!images[current])
                        location.href = `/offer/${objectId}`;
                    http.post(`/add/image/${gallery.model}/${gallery.objectId}`,{image:images[current].get('base64')});
                };
                http.post(`/add/image/${gallery.model}/${gallery.objectId}`,{image:images[current].get('base64')});
            }
            else{
                log(http.json.errors);
            }
        };
        http.post('/edit/Offer/' + this.id,$('#form').serializeJSON());
    }
}