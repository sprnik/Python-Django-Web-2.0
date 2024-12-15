"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('afisha/category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('afisha/event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('links/', views.links, name='links'),
    path('pool/', views.pool, name='pool'),
    path('registration/', views.registration, name='registration'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),
    path('videopost/', views.videopost, name='videopost'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:event_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:event_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_delete/<int:order_id>/', views.order_delete, name='order_delete'),
    path('update_order_item/<int:item_id>/', views.update_order_item, name='update_order_item'),
    path('add_order_item/<int:order_id>/', views.add_order_item, name='add_order_item'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
