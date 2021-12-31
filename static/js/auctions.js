class Auctions{
    constructor(){
        this.model = 'Auction';
        $('#auctions').addClass(storage.getItem('auctionsViewMode') ? storage.getItem('auctionsViewMode') : 'dvm-auctions-full-mode');
    }
}

var view = new Auctions();