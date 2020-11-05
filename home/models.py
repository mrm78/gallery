from django.db import models
from utils.date_convertor import gregorian_to_shamsi

class article(models.Model):
    topic = models.BinaryField()
    text = models.BinaryField()
    date = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='article_images', default='a.jpg')
    presentor = models.BinaryField()
    view_counter = models.IntegerField(default=0)
    def shamsi_date(self):
        return gregorian_to_shamsi(self.date)

class article_comment(models.Model):
    text = models.BinaryField(default=b'good!')
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    article = models.ForeignKey(article, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    def shamsi_date(self):
        return gregorian_to_shamsi(self.date)

