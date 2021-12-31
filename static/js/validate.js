class Validator{
    constructor(form,rules){
        this.valid = [];
        this.invalid = [];
        this.form = form;
        this.rules = rules;
        this.form.validateSubmit = this.form.find('#submit');
        this.form.valid = false;

        this.form.on('submit',this.submit);

        for(let[key,rulesList] of Object.entries(rules)){
            this.listenRules(this.form.find(`[name=${key}]`)[0],rulesList);
        }
    }
    listenRules(elem,rule){
        elem.on(rule['event'] ? rule['event'] : 'paste keydown focusout',function(event){
            var elem = this;

            if(elem.timeout)
                clearTimeout(elem.timeout);

            if(event.type == 'focusout'){
                if(!elem.value)
                    validator.error(elem,rule['errors']['required']);
                else if(elem.invalid){
                    return false;
                }
            }

            elem.removeError();
            elem.invalid = false;

            elem.timeout = setTimeout(function(){
                validator.validate(elem,rule);
                if(!elem.invalid && rule['unique'])
                    validator.unique(elem,rule['errors']['unique']);
            },rule['timeout'] ? rule['timeout'] : 1500);

            event.stopPropagation();
            return false;
        });
    }
    validate(elem,rules){
        for(let[key,rule] of Object.entries(rules['rules'])){
            var result = this[key](elem,rule);
            if(result){
                this.pop(elem);
                if(!this.invalid.length)
                    this.form.triggerValid();
            }else{
                this.error(elem,rules['errors'][key]);
            }
        }
    }
    submit(event){
        for(let[key,rule] of Object.entries(rules)){
            var elem = validator.form.find(`[name=${key}]`)[0];
            validator.validate(elem,rule);
            if(!elem.invalid && rule['unique'])
                validator.unique(elem,rule['errors']['unique']);
        }
        if(!Array.isArray($("#g-recaptcha-response")) && !$("#g-recaptcha-response").value){
            event.preventDefault();
            event.stopPropagation();
            return false;
        }

        if(validator.invalid.length){
            validator.invalid[0].focus();
            event.preventDefault();
            event.stopPropagation();
            return false;
        }
    }
    equal(elem,rule){
        if(elem.value != this.form.find(`[name=${rule}]`)[0].value)
            return false;
        return true;
    }
    min_length(elem,rule){
        if(elem.value.length < rule)
            return false;
        return true;
    }
    max_length(elem,rule){
        if(elem.value.length > rule)
            return false;
        return true;
    }
    regex(elem,rule){
        var match = elem.value.match(rule);
        if(!match)
            return false;
        return true;
    }
    unique(elem,error){
        http.action = function(){
            if(http.json && !http.json.result){
                validator.error(elem,error);
                if(!validator.invalid.length)
                    validator.form.triggerValid();
            }
        };
        http.post('/match/user',{email:elem.value});
    }
    push(elem){
        if(!this.invalid.includes(elem))
            this.invalid.push(elem);
        if(this.valid.includes(elem))
            this.valid.pop(elem);
        elem.invalid = true;
    }
    pop(elem){
        if(!this.valid.includes(elem))
            this.valid.push(elem);
        if(this.invalid.includes(elem))
            this.invalid.pop(elem);
        elem.invalid = false;
    }
    error(elem,error){
        elem.triggerError(error);
        this.push(elem);
    }
}