from datetime import datetime

from django.db import models

# Create your models here.


class UserLog(models.Model):
    location = models.TextField(null=True)
    address = models.TextField(null=True)
    x = models.TextField(null=True)
    y = models.TextField(null=True)
    log_date = models.DateTimeField(default=datetime.now())
    weather = models.TextField(null=True)
    log_type = models.TextField(null=True)
    contents = models.TextField()
    # item = models.TextField()
    user_id = models.IntegerField()

    class Meta:
        db_table = 'userlog'

    def __str__(self):
        return f"{self.pk}"
        # return f'[{self.pk}] 위치 : {self.location},' \
        #        f'주소 : {self.address},' \
        #        f'위도 : {self.x},' \
        #        f'경도 : {self.y},' \
        #        f'로그 생성 날짜 : {self.log_date},' \
        #        f'날씨 : {self.weather},' \
        #        f'로그 타입 : {self.log_type},' \
        #        f'내용 : {self.contents},' \
        #        f'주요 내용 : {self.item},' \
        #        f'사용자 : {self.user_id}'
