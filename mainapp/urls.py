from django.urls import path, re_path

from .views import Index
from .views import domain_info

app_name = 'mainapp'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    re_path(r'^domain/(?P<domain>\w{0,50})$', domain_info),
]
