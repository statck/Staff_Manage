"""
URL configuration for day16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from staff_manage import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # 部门管理
    path('depart/list/' , views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    # 使用正则表达式传入nid
    # http://127.0.0.1:8080/depart/1/edit
    path('depart/<int:nid>/edit/' , views.depart_edit),
    # 用户管理
    path('user/list/',views.user_list),
    path('user/add/',views.user_add),
    path('user/model/form/add/',views.user_model_form_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),

]
