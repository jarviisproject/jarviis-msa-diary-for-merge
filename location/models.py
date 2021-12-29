
from django.db import models

# Create your models here.


class LocationData(models.Model):
    # location,category,address
    location = models.TextField()
    category = models.TextField()
    address = models.TextField()

    class Meta:
        db_table = 'location'

    def __str__(self):
        return f'{self.pk, self.location, self.category, self.address}'

    # def __str__(self):
    #     return f'[{self.pk}] 위치 : {self.location},' \
    #            f'카테고리 : {self.category},' \
    #            f'주소 : {self.address}'


