# from django import forms
# from django.contrib import admin
# from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.contrib.auth import get_user_model
# from user_auth.forms import AuthUserCreationForm
# from user_auth.forms import AuthForm as AuthenticationForm
# from user_auth.forms import AuthUserChangeForm

# class UserCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = get_user_model()
#         fields = (
#             'email', 
#             'first_name', 
#             'last_name',
#             'is_active', 
#         )

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
    
#     def clean_email(self):
#         email = self.cleaned_data.get('email')    
#         email_exists = get_user_model().objects.filter(email__exact=email)
#         if email_exists:
#             raise forms.ValidationError('This email already exists in our database')
#         return email
    
#     def clean_mobile_number(self):
#         mobile_number = self.cleaned_data.get('mobile_number')    
#         mobile_number_exists = get_user_model().objects.filter(mobile_number__exact=mobile_number)
#         if email_exists:
#             raise forms.ValidationError('This mobile number already exists in our database')
#         return email

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. 
    
#     Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = get_user_model()
#         fields = (
#             'first_name',
#             'last_name',
#             'is_active', 
#         )
    
# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserChangeForm
#     add_form = UserCreationForm

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on user_auth.User.
#     list_display = (
#         '__str__',
#         'email',
#         'first_name',
#         'last_name',
#         'is_admin',
#         'is_active',
#         'mobile_number'
#     )
#     list_filter = ('is_admin', 'is_active' )
#     list_per_page = 25
#     fieldsets = (
#         (None, {'fields': ('mobile_number', 'email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_admin', 'is_active')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (
#             None, 
#             {
#                 'classes': ('wide',),
#                 'fields': (
#                     'email',
#                     'mobile_number', 
#                     'first_name', 
#                     'last_name', 
#                     'password1', 
#                     'password2', 
#                     'is_admin',
#                     'is_active'
#                 )
#             }   
#         ),
#     )
#     search_fields = (
#         'email',
#         'mobile_number',
#         'first_name', 
#         'last_name',
#     )
#     ordering = ('first_name', 'last_name')
#     filter_horizontal = ()


# class LaceAdminSite(admin.AdminSite):
#     site_header = 'Lace Admin'
#     site_title = 'Admin Site'
#     index_title = 'Lace'
#     login_template = 'user_auth/admin_login.html'
#     login_form = AuthenticationForm
    
# # Now register the new UserAdmin...
# admin_site = LaceAdminSite(name='console')
# admin_site.register(get_user_model(), UserAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin_site.unregister(Group)



