from django.contrib import admin

from django.contrib import admin
from django import forms
from pagedown.widgets import AdminPagedownWidget
from blog.models import Category, Article, LikePost


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', )
    search_fields = ('name', )
    fieldsets = (
        (
            None,
            {
                'fields': ('name', 'slug',)
            }
        ),
    )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        widgets = {
            'content': AdminPagedownWidget(),
        }


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'published', 'created_at', 'updated_at')
    search_fields = ('name', 'content', 'published', 'created_at', 'updated_at')
    list_filter = ('categories', 'published')
    fieldsets = (
        (
            None,
            {
                'fields': ('name', 'slug', 'short_content', 'content',
                           'categories', 'published')
            }
        ),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(LikePost)

