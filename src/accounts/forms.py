from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()

        if username and password:
            user = authenticate(username=username, password=password)
            #print (user)
            if not user:
                raise forms.ValidationError("El usuario no existe")
            if not user.check_password(password):
                raise forms.ValidationError("Contraseña incorrecta")
            if not user.is_active:
                raise form.ValidationError("El usuario esta inactivo")

        return super(UserLoginForm, self).clean(*args, **kwargs)
