var rules = {
    'email':{
        'required': true,
        'rules':{
            'regex':/[a-zA-Z0-9\-\_]+@[a-z0-9]+\.[a-z]{2,3}/,
        },
        'unique':true,
        'errors':{
            'regex':'Неправильный email',
            'unique':'email уже занят'
        }
    },
    'fname':{
        'required': true,
        'rules':{
            'min_length':2,
            'regex':/[а-яА-Яa-zA-Z0-9\-\_\.]/,
        },
        'errors':{
            'min_length':'Минимальная длина 2 символов',
            'regex':'Неправильный ввод'
        }
    },
    'lname':{
        'required': true,
        'rules':{
            'min_length':2,
            'regex':/[а-яА-Яa-zA-Z0-9\-\_\.]/,
        },
        'errors':{
            'min_length':'Минимальная длина 2 символов',
            'regex':'Неправильный ввод'
        }
    },
    'password1':{
        'required': true,
        'rules':{
            'min_length':6,
        },
        'errors':{
            'min_length':'Минимальная длина 6 символов',
        }
    },
    'password2':{
        'required': true,
        'rules':{
            'min_length':6,
            'equal':'password1',
        },
        'errors':{
            'min_length':'Минимальная длина 6 символов',
            'equal':'Пароли не совпадают',
        }
    }
};

validator = new Validator($('#form'),rules);