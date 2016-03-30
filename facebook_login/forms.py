from django import forms
from django.contrib.auth.models import User


class EmailForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control input_width', 'required': 'required'})

    # def clean_email(self):
    #     try:
    #         existing_user = User.objects.get(email__iexact=self.cleaned_data['email'])
    #         if existing_user:
    #             self._errors["email"] = self.error_class(["An account already exists under this email address. Please use the forgot password function to log in."])
    #     except User.MultipleObjectsReturned:
    #         self._errors["email"] = self.error_class(["An account already exists under this email address. Please use the forgot password function to log in."])
    #     except:
    #         pass
    #
    #     return self.cleaned_data['email']
