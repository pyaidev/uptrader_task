from django.contrib import admin

from menu.models import Page, Menu, MenuPage


class PageAdmin(admin.ModelAdmin):
    model = Page
    list_display = ['id', 'title', 'title_in_menu']
    list_display_links = ['id', 'title']


class MenuPagesInline(admin.TabularInline):
    model = MenuPage
    extra = 0


class MenuAdmin(admin.ModelAdmin):
    model = Menu
    list_display = ['id', 'title', 'slug']
    list_display_links = ['id', 'title']
    inlines = [MenuPagesInline]


admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)
