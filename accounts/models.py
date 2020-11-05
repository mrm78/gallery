from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random
from string import ascii_letters
from orders.views import product
from utils.date_convertor import gregorian_to_shamsi

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, phone, name, password):
        email = self.normalize_email(email)
        #create invite code
        invite_code = ''.join(random.choice(ascii_letters) for i in range(10))
        while user.objects.filter(invite_code=invite_code):
            invite_code = ''.join(random.choice(ascii_letters) for i in range(10))
        User = self.model(email=email, phone=phone, name=name, invite_code=invite_code)
        User.set_password(password)
        User.save(using=self._db)
        return User
 
class user(AbstractUser): 
    phone = models.CharField(max_length=15, unique=True, null=True)
    verified_phone = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    verified_email = models.BooleanField(default=False)
    verification_code = models.IntegerField(null=True, blank=True)
    verification_code_time = models.DateTimeField(auto_now=True)
    invite_code = models.CharField(max_length=10, unique=True, null=True)
    introducer = models.ForeignKey('user', null=True, blank=True,related_name='invited_set' , on_delete=models.SET_NULL)
    date_joined = models.DateTimeField(auto_now=True)
    first_name = None
    last_name = None
    username = None
    name = models.BinaryField(default=b'A')
    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def has_product(self, ID):
        Product = product.objects.filter(id=ID)
        if not Product:
            return False
        for order in self.order_set.all():
            if order.product.id == ID and order.paid:
                return True

    def shamsi_date(self):
        return gregorian_to_shamsi(self.date_joined)

    def paid_orders(self):
        orders = []
        for o in self.order_set.all():
            if o.paid: 
                orders.append(o)
        return orders
        