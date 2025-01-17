"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web_tool import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('hello/', views.hello_world), #新增網址與對應的動作 #http://localhost/hello/
    path('ana_stock/', views.analyze_stock, name='analyze_stock'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('api/stock-data/', views.get_stock_data, name='get_stock_data'),
    path('stock_data/', views.show_stock_data, name='show_stock_data'),
    path('save_stock/', views.save_stock, name='save_stock'),
    path('analyze_stock/',views.analyze_stock, name='analyze_stock'),
    path('check_save/', views.check_save, name='check_save'),
    path('delete_stock/', views.delete_stock, name='delete_stock'),
]
