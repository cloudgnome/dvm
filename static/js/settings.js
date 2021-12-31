function saveImage(input,base64){
    http.action = function(){};
    http.post('/user/add/image',{image:base64});
}
function renderImage(){
    var file = this.files[0];
    var reader = new FileReader();
    var input = this;
    var image = $('label[for="editImage"] img')[0];
    reader.onload = function(e){
        image.src = e.target.result;
        image.set('original',e.target.result);
        input.set('name','images');
        input.set('value',e.target.result);
        saveImage(input,e.target.result);
    };
    reader.readAsDataURL(file);
}

$('#editImage').on('change',renderImage);
