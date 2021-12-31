class Offers{
    constructor(){
        this.model = 'Offer';
        $('#offers').addClass(storage.getItem('offersViewMode') ? storage.getItem('offersViewMode') : 'dvm-offers-full-mode');
    }
}

var view = new Offers();