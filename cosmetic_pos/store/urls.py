from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
]
