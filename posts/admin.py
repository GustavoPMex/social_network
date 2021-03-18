from django.contrib import admin
from .models import PostUser

# Register your models here.

class PostUserAdmin(admin.ModelAdmin):
    readonly_fields = ('date_post', )


admin.site.register(PostUser, PostUserAdmin)

