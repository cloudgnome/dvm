var rules = {
    'email':{
        'required': true,
        'rules':{
            'regex':/[a-zA-Z0-9\-\_]+@[a-z0-9]+\.[a-z]{2,3}/,
        },
        'errors':{
            'regex':'Неправильный email',
            'required':'Обязательное поле'
        }
    }
};

validator = new Validator($('#form'),rules);