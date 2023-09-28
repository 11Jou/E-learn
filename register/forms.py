from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}) , required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) , required=True)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}) , required=True)
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}) , required=True)
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Email'}) , required=True)
    photo = forms.ImageField(required=True , label="Profle Picture")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) , required=True)




