from django.db import models
from utils.date_convertor import gregorian_to_shamsi
import json

class product(models.Model):
    summary = models.BinaryField(null=True, blank=True)
    name = models.BinaryField()
    date = models.DateTimeField(auto_now=True)  #the date of product creation
    File = models.FileField(upload_to='products_files')
    image = models.FileField(upload_to='products_images', default='b.png')
    time = models.BinaryField(default=b"12:45")  #the time of product
    presentor = models.BinaryField(default=b'unknown')
    videos_number = models.IntegerField(default=1)
    price = models.IntegerField(default=54000)
    off = models.FloatField(default=0)
    download_counter = models.IntegerField(default=0)
    def real_price(self):
        return int((1-self.off)*self.price)
    def shamsi_date(self):
        return gregorian_to_shamsi(self.date)
    def percent_off(self):
        return int(self.off * 100)
    def __str__(self):
        return f'{self.id}. ' + self.name.decode()

class order(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    RefID = models.CharField(max_length=30, null=True, blank=True)
    Authority = models.CharField(max_length=45, null=True, blank=True)
    payment_date = models.TimeField(blank=True, null=True)


class comment(models.Model):
    text = models.BinaryField(default=b'good!')
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    def shamsi_date(self):
        return gregorian_to_shamsi(self.date)

class session(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    topic = models.BinaryField(default=b'')
    number = models.IntegerField()
    time = models.BinaryField(default=b'')
