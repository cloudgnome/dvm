class View{
    constructor(){
        var offersViewMode = storage.getItem('offersViewMode') ? storage.getItem('offersViewMode') : 'dvm-offers-full-mode';
        var auctionsViewMode = storage.getItem('auctionsViewMode') ? storage.getItem('auctionsViewMode') : 'dvm-auctions-full-mode';
        $(`div[value=${offersViewMode}]`)[0].addClass('active');
        $(`div[value=${auctionsViewMode}]`)[0].addClass('active');

        $('.dvm-icon-block').on('click touch',this.changeViewMode);
    }
    changeViewMode(event){
        storage.setItem(this.get('name'),this.get('value'));
        this.parent().find('.dvm-icon-block.active').removeClass('active');
        this.addClass('active');
    }
}

var view = new View();