from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator 
from django.core.validators import validate_email
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

class AuthSetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        validators=[MinLengthValidator(8, 'Password must have 8 characters')],
        widget = forms.PasswordInput(
            attrs = {
                'class':'form-control',
                'placeholder':'New Password (Minimum of 8 characters)',
                'min_length': 8,
                'max_length': 255,
                'autofocus': 'on',
            }
        ),
        required = True,
        help_text = 'Password is required'
    )
    new_password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class':'form-control',
                'placeholder':'Confirm New Password (Must match new password)',
                'min_length': 8,
                'max_length':255,
            }
        ), 
        required = True,
        help_text = 'Confirm password must match password'
    )

    class Meta:
        model = get_user_model()
        fields = (
            'password',
        )
    
    def clean_password2(self):
        """Function to check that the two password entries match"""
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and ( password1 != password2 ):
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        """Function to save the provided password in hashed format"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user
    
class AuthUserSignupForm(forms.Form):
    first_name = forms.CharField( 
        widget = forms.TextInput(
            attrs = {
                'id': 'first_name',
                'placeholder':_('First Name'),
                'autocomplete':'off',
                'minlength':2,
                'maxlength':50,
                'oninput': "this.className = ''",
            }
        ),
        required = True,
        label = '',
    )
    last_name = forms.CharField( 
        widget = forms.TextInput(
            attrs = {
                'id': 'last_name',
                'placeholder':_('Last Name'),
                'autocomplete':'off',
                'minlength':2,
                'maxlength':50,
                'oninput': "this.className = ''",
            }
        ),
        required = True,
        label = '',
    )
    gender = forms.ChoiceField( 
        widget = forms.Select(
            attrs = {
                'id': 'gender',
                'maxlength':50,
            }
        ),
        choices = (('M', _('I am Male')), ('F', _('I am Female'))),
        required = True,
        label = '',
    )    
    mobile_number = forms.CharField( 
        widget = forms.TextInput(
            attrs = {
                'id': 'mobile_number_signup',
                'placeholder':_('Mobile Number'),
                'autocomplete':'off',
                'minlength':11,
                'maxlength':11,
                'oninput': "this.className = ''",
            }
        ),
        required = True,
        label = '',
    )
    password = forms.CharField(
        validators=[MinLengthValidator(8, 'Password must have 8 characters')],
        widget = forms.PasswordInput(
            attrs = {
                'id': 'password1',
                'class':'form-control',
                'placeholder':'Password',
                'min_length': 8,
                'max_length': 255,
                'autofocus': 'on',
                'oninput': "this.className = ''",
            }
        ),
        required = True,
        label = '',
    )
    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'id': 'password2',
                'class':'form-control',
                'placeholder':'Confirm Password',
                'min_length': 8,
                'max_length':255,
                'oninput': "this.className = ''",
            }
        ), 
        required = True,
        label = '',
    )
    # location = forms.CharField( 
    #     widget = forms.TextInput(
    #         attrs = {
    #             'id': 'location',
    #             'placeholder':_('Location'),
    #             'autocomplete':'off',
    #             'minlength':2,
    #             'maxlength':255,
    #             'oninput': "this.className = ''",
    #         }
    #     ),
    #     required = True,
    #     label = '',
    # )
    
    def clean_password2(self):
        """Function to check that the two password entries match"""
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and ( password1 != password2 ):
            raise forms.ValidationError('Passwords don\'t match')
        return password2
    
class AuthUserLoginForm(forms.Form):
    username = forms.CharField( 
        widget = forms.TextInput(
            attrs = {
                'id': 'mobile_number',
                'placeholder':_('Mobile Number'),
                'autocomplete':'off',
                'autofocus':'on',
                'minlength':11,
                'maxlength':11,
            }
        ),
        required = True,
        label = '',
    )
    password = forms.CharField( 
        widget = forms.PasswordInput(
            attrs = {
                'id': 'password',
                'placeholder':_('Password'),
                'autocomplete':'off',
                'minlength':8,
                'maxlength':255,
            }
        ),
        required = True,
        label = '',
    )
 

class AuthPasswordResetForm(forms.Form):
    mobile_number = forms.CharField( 
        widget = forms.TextInput(
            attrs = {
                'id': 'mobile_number_reset',
                'placeholder':_('Mobile Number'),
                'autocomplete':'off',
                'autofocus':'on',
                'minlength':11,
                'maxlength':11,
            }
        ),
        required = True,
        label = '',
    )
    email = forms.EmailField(
        validators=[validate_email],
        widget = forms.EmailInput(
            attrs = {
                'id': 'email',
                'placeholder':_('Email'),
                'autocomplete':'off',
                'autofocus': True,
                'minlength':5,
                'maxlength':191,
            }
        ),
        required = True,
        label = '',
    )   
    
