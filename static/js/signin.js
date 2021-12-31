var rules = {
    'login':{
        'required': true,
        'rules':{
            'regex':/[a-zA-Z0-9\-\_]+@[a-z0-9]+\.[a-z]{2,3}/,
        },
        'errors':{
            'regex':'Неправильный email',
            'required':'Обязательное поле'
        }
    },
    'password':{
        'required': true,
        'rules':{
            'min_length':6,
        },
        'errors':{
            'min_length':'Минимальная длина 6 символов',
            'required':'Обязательное поле'
        }
    }
};

validator = new Validator($('#form'),rules);