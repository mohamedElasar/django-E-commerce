from django.urls import path
from .views import checkout, HomeView ,ItemDetailView

app_name = 'core'

urlpatterns = [
    path('product/<slug>', ItemDetailView.as_view(),name = 'products-page'),
    path('checkout/', checkout,name = 'checkout-page'),
    path('', HomeView.as_view(),name = 'starting-page'),

]
