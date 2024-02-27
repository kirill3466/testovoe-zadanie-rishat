from django.urls import path

from . import views

urlpatterns = [
    path('buy/<int:item_id>', views.buy, name='buy'),
    path('buy_order/<int:order_id>', views.buy_order, name='buy_order'),
    path(
        'payment_intent/<int:order_id>',
        views.payment_intent,
        name='payment_intent'
    ),

    path('item/<int:id>', views.get_item, name='item'),
    path('order/<int:id>', views.get_order, name='order'),

    path('success/', views.SuccesView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),

    path('', views.IndexView.as_view(), name='index'),
]
