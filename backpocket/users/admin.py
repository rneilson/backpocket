from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import PermissionDenied

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = []

    def __init__(self, *args, requser=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._requser = requser

    def clean(self):
        super().clean()
        return self.cleaned_data

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = []

    def __init__(self, *args, requser=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._requser = requser

    def clean(self):
        super().clean()
        return self.cleaned_data

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'name', 'email', 'is_staff')
    list_filter = ('is_superuser', 'is_active', 'groups')
    fieldsets = (
        (
            None,
            {'fields': ('id', 'date_joined', 'last_login',)}
        ),
        (
            'Personal info',
            {'fields': ('username', 'name', 'email',)}
        ),
        (
            'Permissions',
            {'fields': ('is_active', 'groups', 'user_permissions',)}
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'password1',
                    'password2',
                    'name',
                    'email',
                ),
            }
        ),
    )
    search_fields = ('name', 'username', 'email')
    ordering = ('name', 'username', 'email')
    filter_horizontal = ('user_permissions', 'groups',)

    readonly_fields = ('id', 'date_joined', 'last_login',)
    _readonly_field_perms = {
        'set_user_active': ('is_active',),
        'change_user_groups': ('groups',),
        'change_user_permissions': ('user_permissions',),
        'change_user': ('username', 'name', 'email',),
    }

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        readonly = list(self.readonly_fields)

        for perm, fields in self._readonly_field_perms.items():
            if not user.has_perm(perm, obj):
                readonly.extend(fields)

        return readonly

    def get_form(self, request, obj=None, **kwargs):
        getter = super().get_form(request, obj, **kwargs)
        requser = request.user

        def formget(*args, **inkwargs):
            inkwargs['requser'] = requser
            return getter(*args, **inkwargs)

        return formget

    def save_model(self, request, obj, form, change):
        # Make sure we can add/change given new obj
        if change:
            if not request.user.has_perm('bp_users.change_user', obj):
                raise PermissionDenied
        else:
            if not request.user.has_perm('bp_users.add_user', obj):
                raise PermissionDenied

        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.has_perm('bp_users.add_user')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('bp_users.change_user', obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('bp_users.delete_user', obj)

