from django.urls import path
from orders.views import download, Product, commenting, payment_request, payment_verify, list_courses

urlpatterns = [
    path('download/<int:ID>', download, name='download'),
    path('product/<int:ID>',Product, name="product"),
    path('commenting', commenting, name='commenting'),
    path('payment_request/<int:ID>', payment_request, name='payment_request'),
    path('payment_verify', payment_verify, name='payment_verify'),
    path('list_courses', list_courses, name='list_courses')
]