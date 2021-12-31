var timeout;
var Validator;
function ValidatorProt(form,rules){
    this.form = form;
    this.form.validateSubmit = this.form.find('#submit');
    this.rules = rules;
    this.valid = [];
    this.invalid = [];
    this.form.valid = true;

    this.form.on('submit',function(event){
        Validator.validate();

        if(!this.valid){
            event.preventDefault();
            event.stopPropagation();
            return false;
        }
    });

    for(let[key,rule] of Object.entries(rules)){
        var elem = this.form.find(`[name=${key}]`)[0];

        this.invalid.push(elem);

        elem.on(rule['event'] ? rule['event'] : 'paste keypress focus focusout',function(event){
            this.removeError();

            if(timeout)
                clearTimeout(timeout);

            var elem = this;

            timeout = setTimeout(function(){
                Validator.validate(elem,rule,event);
            },rule['timeout'] ? rule['timeout'] : 1500);

            event.stopPropagation();
            return false;
        });
    }
}
ValidatorProt.prototype.required = function(event,elem){
    if(event.type == 'focusout' && !elem.value){
        if(!value['required'])
            return;
        elem.triggerError('Обязательное поле');
        this.invalid.push(elem);
        this.valid.pop(elem);
        return;
    }
};
ValidatorProt.prototype.focus = function(event,elem){
    if(!elem.value && event.type == 'focus')
        return;
};
ValidatorProt.prototype.min_length = function(elem){
    if(value['min_length'] && elem.value.length < value['min_length']){
        elem.triggerError(value['errors']['min_length']);
        this.invalid.push(elem);
        this.valid.pop(elem);
        return;
    }
};
ValidatorProt.prototype.max_length = function(elem){
    if(value['max_length'] && elem.value.length < value['max_length']){
        elem.triggerError(value['errors']['max_length']);
        this.invalid.push(elem);
        this.valid.pop(elem);
        return;
    }
};
ValidatorProt.prototype.regex = function(elem){
    if(value['regex']){
        var match = elem.value.match(value['regex']);
        if(!match){
            elem.triggerError(value['errors']['regex']);
            this.invalid.push(elem);
            this.valid.pop(elem);
        }
        return;
    }
};
ValidatorProt.prototype.unique = function(elem){
    var validator = this;
    if(value['unique']){
        http.action = function(){
            if(http.json && !http.json.result){
                elem.triggerError(value['errors']['unique']);
                validator.invalid.push(elem);
                validator.valid.pop(elem);
            }
        };
        http.post('/match/user',{email:match[0]});
        return;
    }
};
ValidatorProt.prototype.validate = function(elem,event){
    elem.removeError();
    validateForm.triggerValid();
};

Element.prototype.validate = function(rules){
    Validator = new ValidatorProt(this,rules);
};