from django.db import models

# Create your models here.
class Location(models.Model):
    # def __init__(self):
    #     self.Location='Location'
    # CharField 一定要给长度
    type1 = models.CharField(max_length = 1000, verbose_name='标题')
    addr = models.CharField(max_length = 1000, verbose_name='地址')
    price = models.CharField(max_length = 500, verbose_name='价格')
    url = models.CharField(max_length = 500,verbose_name='网址')

    def __str__(self):
        return self.name
        
    class Meta:
        db_table = "Location"
        verbose_name = '房源'
        verbose_name_plural = verbose_name