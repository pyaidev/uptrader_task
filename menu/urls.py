from django.urls import path

from menu.views import main_page, get_page

urlpatterns = [
    path('', main_page, name='main_page'),
    path('<int:page_id>/', get_page, name='page')
]
