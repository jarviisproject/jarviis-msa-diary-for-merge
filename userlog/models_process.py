import csv
import random

import requests

from common.models import ValueObject, Reader
from location.models import LocationData
from location.models_process import Location
from location.serializers import LocationSerializer
from userlog.models import UserLog
from weather.models import Weather


class LogData(object):
    def __init__(self):
        vo = ValueObject()
        vo.context = 'location/data/'
        vo.fname = 'location_data.csv'
        reader = Reader()
        # self.printer = Printer()
        self.csvfile = reader.new_file(vo)
        self.weather = Weather()

    def process(self):
        return self.create_log()

    def create_log(self):
        log = self.random_log()
        weather = self.weather.process()
        latlng = Location().getLatLng(log['address'])
        return {'location': log['location'],
                'address': log['address'],
                'x': latlng[0] if log['address'] != '' else '',
                'y': latlng[1] if log['address'] != '' else '',
                'weather': weather,
                'log_type': log['log_type'],
                'contents': log['contents'],
                # 'item': log['item']
                }

    def random_log(self):
        ls = self.dummy_from_db()
        num = random.randint(0 ,len(ls)-1)
        if random.randint(0, 4) == 0:
            return self.create_visit(ls, num)
        elif random.randint(0, 4) == 1:
            return self.create_payment(ls, num)
        elif random.randint(0, 4) == 2:
            return self.create_workout()
        else:
            return self.create_study()
        # return self.create_visit(ls, num) if random.randint(0, 1) == 0 else self.create_payment(ls, num)

    def create_visit(self, ls, num):
        return {'location': ls[num]['location'],
                'address': ls[num]['address'],
                'log_type': 'visit',
                'contents': f"{ls[num]['category']}-{ls[num]['location']}을 방문했다.",
                # 'item': f"{ls[num]['location']} 방문"
                }

    def create_payment(self, ls, num):
        return {'location': ls[num]['location'],
                'address': ls[num]['address'],
                'log_type': 'payment',
                'contents': f"[{ls[num]['category']}] {ls[num]['location']}에서 {random.randint(0 ,1000 ) *100}원을 결제했다.",
                # 'item': f"{random.randint(0 ,1000 ) *100}"
                }

    def create_study(self):
        test = [
            "열심히 자바 공부를 했다.",
            "DB 연결하는 작업을 했는데 어려웠다.",
            "재미있게 파이썬 공부를 하고 개발해봤다.",
            "작업물을 깃허브에 커밋했다.",
        ]
        return {'location': '비트캠프',
                'address': '',
                'log_type': 'study',
                'contents': test[random.randint(0 ,len(test) -1)]
                }

    def create_workout(self):
        test = [
            "땀 날 때까지 조깅을 했다.",
            "천천히 걷기 운동을 했다.",
            "친구들과 배드민턴을 하고 놀았다.",
            "마라톤 연습을 했다.",
        ]
        return {'location': '올림픽공원',
                'address': '',
                'log_type': 'workout',
                'contents': test[random.randint(0 ,len(test) -1)]
                }

    def dummy_from_csv(self):
        ls = []
        with open(self.csvfile, newline='', encoding='utf8') as f:
            [ls.append(i) for i in csv.DictReader(f)]
        return ls

    def dummy_from_db(self):
        ls = []
        data = LocationData.objects.all()
        serializer = LocationSerializer(data, many=True)
        [ls.append(dict(i)) for i in serializer.data]
        return ls