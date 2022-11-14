from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from gallery.models import Price,Plant,Photo
class ProfileInline(admin.StackedInline):
    model=Profile
    can_delete =True
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines =(ProfileInline,)

    
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Price)
admin.site.register(Plant)
admin.site.register(Photo)

# Register your models here.
