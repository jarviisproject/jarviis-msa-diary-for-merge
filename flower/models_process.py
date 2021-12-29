import os
import random
from datetime import datetime
from konlpy.tag import Okt


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
import django
django.setup()
from userlog.models import UserLog
from routine.models import Routine
from flower.models import Flower


class FlowerMaker:
    def __init__(self):
        pass

    def process(self, user_id):
        # Getting ALL of today logs
        today = datetime.now().date()
        today_routines = list(Routine.objects.filter(create_date__year=today.year,
                                                 create_date__month=today.month,
                                                 create_date__day=today.day,
                                                 user_id=user_id).values())

    def create_flower(self, contents, log_id, user_id):
        # new flower
        Flower.objects.create(title=' '.join(contents),
                              grade=0,
                              step=1,
                              color=["RED", "BLUE", "YELLOW"][random.randint(0, 2)],
                              log_id=[log_id],
                              user_id=user_id
                              )

    def update_flower(self, flower, log_id):
        # update Flower
        # flower = Flower.objects.get(title__iexact=routine_contents)
        print("********* update flower **********")
        print(f"flower :: {flower}")
        print(f"flower.log_id :: {flower.log_id}")
        flower.log_id.append(log_id)
        print(f"flower.log_id :: {flower.log_id}")
        print(f"flower.log_id type :: {type(flower.log_id)}")
        flower_log = flower.log_id
        flower.log_id = list(set(flower_log))
        flower.save()
        flower.step = flower.step + 1 if flower.step < 27 else flower.step
        flower.save()
        if flower.step < 3:
            flower.grade = 0
        elif flower.step < 6:
            flower.grade = 1
        elif flower.step < 10:
            flower.grade = 2
        elif flower.step < 15:
            flower.grade = 3
        elif flower.step < 21:
            flower.grade = 4
        elif flower.step < 28:
            flower.grade = 5
        flower.save()