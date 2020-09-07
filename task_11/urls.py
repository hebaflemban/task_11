"""task_11 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from restaurants import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('restaurants/list/',views.restaurant_list ,name='restaurant-list'),
    path('restaurants/<int:restaurant_id>/detail/',views.restaurant_detail ,name='restaurant-detail'),

    path('restaurants/create/',views.restaurant_create ,name='restaurant-create'),
    path('restaurants/<int:restaurant_id>/update/',views.restaurant_update ,name='restaurant-update'),
    path('restaurants/<int:restaurant_id>/delete/',views.restaurant_delete ,name='restaurant-delete'),

    path('restaurants/<int:restaurant_id>/item/add/',views.item_create ,name='item-create'),

    path('signup/',views.signup ,name='signup'),
    path('signin/',views.signin ,name='signin'),
    path('signout/',views.signout ,name='signout'),

    path('denied/',views.no_access ,name='no_access'),

]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
