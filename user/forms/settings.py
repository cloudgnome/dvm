from .auth import SignUpForm
from django import forms
from user.models import User
from form_utils.forms import BetterModelForm

class SettingsForm(SignUpForm,BetterModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, *args, commit = True, **kwargs):
        user = super().save(*args, **kwargs)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

    class Meta:
        fields = '__all__'
        model = User
        exclude = ('password','social_type','social_id','is_active','image','balance')
        fieldsets = [
                    ('', {'fields':['fname','lname'],'legend':''}),
                    ('', {'fields':['email','phone'],'legend':''}),
                    ('', {'fields':['password1','password2'],'legend':''}),
                ]