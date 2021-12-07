from django.contrib import admin

from main.models import Category, Image, Post, CommentPost


# Register your models here.
class ImageInLineAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 7

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLineAdmin, ]

admin.site.register(Category)
admin.site.register(CommentPost)
