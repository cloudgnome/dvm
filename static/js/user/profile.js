$('.dropdown').on('click touch',function(event){
    this.toggleMenu({
        'parent':$('#load'),
        'timeout':200
    });
});