from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import User


# Register your models here.


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone_number',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone_number',)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = User

    list_display = ('phone_number', 'name', 'email', 'is_active', 'verification_code', 'phone_number_verified',
                    'is_staff', 'is_superuser', 'last_login', 'phone_number_verified')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': (
            'name', 'password', 'phone_number',)}),
        ('Permissions', {'fields': (
            'is_staff', 'is_active', 'receive_notifications', 'receive_promotions', 'receive_email_notifications',
            'is_superuser', 'phone_number_verified', 'groups', 'user_permissions')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 'phone_number', 'email', 'password1', 'password2', 'is_staff',
                'is_active', 'is_superuser', 'phone_number_verified',)}
         ),
    )
    search_fields = ('name', 'phone_number', 'email',)
    ordering = ('name',)


admin.site.register(User, CustomUserAdmin)
