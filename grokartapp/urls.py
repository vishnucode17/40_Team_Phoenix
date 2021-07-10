from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'grokartapp'
urlpatterns=[
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('add_product',views.add_product,name='add_product'),
    path('search/',views.search,name='search'),
    path('products/<slug:slug>',views.product_view,name="product_view"),
    path('cart/<slug:slug>/',views.add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<slug:slug>',views.remove_from_cart,name='remove_from_cart'),
    path('mycart/',views.cart,name='cart'),
    path('order_summary/',views.order_summary,name='order_summary'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)