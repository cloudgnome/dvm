var rules = {
    'email':{
        'required': true,
        'rules':{
            'regex':/[a-zA-Z0-9\-\_]+@[a-z0-9]+\.[a-z]{2,3}/,
        },
        'errors':{
            'regex':'Неправильный email'
        }
    },
    'name':{
        'required': true,
        'rules':{
            'min_length':2,
            'regex':/[а-яА-Яa-zA-Z0-9\-\_\.]/,
        },
        'errors':{
            'min_length':'Минимальная длина 2 символов',
            'regex':'Неправильный ввод'
        }
    }
};

validator = new Validator($('#form'),rules);
gallery = new Gallery(model='Business');