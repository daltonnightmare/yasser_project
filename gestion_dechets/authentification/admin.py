from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# Register your models here.
@admin.register(User)
class UserAdministration(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_citoyen', 'is_entreprise', 'is_municipalite')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_citoyen', 'is_entreprise', 'is_municipalite')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
    )
   