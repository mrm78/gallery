from django.contrib import admin
from .models import product, order, comment, session

admin.site.register(product)
admin.site.register(order)
admin.site.register(comment)
admin.site.register(session)