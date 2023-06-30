from django.contrib import admin
from .models import Creator, EndUser, Post, Message, Bid
# Register your models here.
from django.contrib.auth.admin import UserAdmin
class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'username','first_name')
    ordering = ('email',)
    list_display = ('email', 'username', 'firstname')

    fieldsets = (
        ('Demographics', {'fields': ('email', 'username', 'first_name')}),

    )



admin.site.register(Creator)
admin.site.register(EndUser)
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Bid)