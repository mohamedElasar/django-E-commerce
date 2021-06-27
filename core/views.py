from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib import messages


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
            order.save()
            messages.info(request,'this item quantity was updated')
            return redirect ('core:products-page', slug = slug)
        else:
            order.items.add(order_item)
            order.save()
            messages.info(request,'this item was added to your cart')
            return redirect ('core:products-page', slug = slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.info(request,'this item was added to your cart')
        return redirect ('core:products-page', slug = slug)


def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:products-page",slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:products-page", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:products-page", slug=slug)
