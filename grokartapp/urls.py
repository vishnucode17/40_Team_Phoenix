from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('add_product',views.add_product,name='add_product')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)