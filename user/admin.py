from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label = '비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label = '비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('nickname', 'email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"../password/\">this form</a>."
    )

    class Meta:
        model = User
        fields = ('nickname', 'email', 'password', 'is_active', 'is_staff', 'is_admin')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'nickname', 'email', 'is_admin', 'is_staff', 'is_active')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('nickname', 'email', 'password1', 'password2')}
         ),
    )
    search_fields = ('nickname', 'email', )
    ordering = ('-id', 'nickname', 'email')
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)