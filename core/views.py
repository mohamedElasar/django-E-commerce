from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone



def checkout(request):
    return render(request,'checkout-page.html')

class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'
    context_object_name = 'items'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'
    context_object_name = 'item'


def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item , created= OrderItem.objects.get_or_create( # this return tuple
    user= request.user,
    ordered = False,
    item=item
    )
    order_qs = Order.objects.filter(user = request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect ('core:products-page', slug = slug)
