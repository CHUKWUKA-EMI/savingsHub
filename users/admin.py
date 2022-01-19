from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name','password', 'phone_number', 
    'home_address','country', 'gender', 'employment_status', 'date_of_birth')


admin.site.register(User, UserAdmin)