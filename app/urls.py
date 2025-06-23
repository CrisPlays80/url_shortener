from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('shorten', views.shorten, name='shorten'),
    # path('url/<str:short_code>', views.redirect_to_url, name='redirect_to_url'),
    # path('url/<str:short_code>/details', views.url_detail, name='url_detail'),
]