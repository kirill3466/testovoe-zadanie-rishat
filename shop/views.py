import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from settings import settings

from .models import Item, Order

stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
PUBLIC_KEY = settings.STRIPE_API_KEY_PUBLISHABLE


def buy(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return JsonResponse({
        'session_id': session.id,
    })


def buy_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    line_items = [{
        'price_data': {
            'currency': item.currency,
            'product_data': {
                'name': item.name,
            },
            'unit_amount': int(item.price * 100),
        },
        'quantity': item.quantity,
    } for item in order.items.all()]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return JsonResponse({
        'session_id': session.id,
    })


def payment_intent(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    line_items = [{
        'price_data': {
            'currency': item.currency,
            'product_data': {
                'name': item.name,
            },
            'unit_amount': int(item.price * 100),
        },
        'quantity': item.quantity,
    } for item in order.items.all()]

    payment_intent = stripe.PaymentIntent.create(
        amount=sum(
            item['price_data']['unit_amount'] * item['quantity'] for item in line_items
        ),
        currency=order.items.first().currency,
        automatic_payment_methods={"enabled": True},
    )

    return JsonResponse({
        'client_secret': payment_intent['client_secret'],
    })


def get_item(request, id):
    item = Item.objects.get(pk=id)
    context = {
        'item': item,
        'stripe_key': settings.STRIPE_API_KEY_PUBLISHABLE,
    }
    return render(request, 'shop/item.html', context)


def get_order(request, id):
    order = Order.objects.get(pk=id)
    context = {
        'order': order,
        'stripe_key': settings.STRIPE_API_KEY_PUBLISHABLE,
    }
    return render(request, 'shop/order.html', context)


class IndexView(TemplateView):
    template_name = 'shop/base.html'


class SuccesView(TemplateView):
    template_name = 'shop/result/success.html'


class CancelView(TemplateView):
    template_name = 'shop/result/cancel.html'
