import random
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import manhattan_distances
from sklearn.metrics.pairwise import cosine_similarity
import os


from konlpy.tag import Okt

from flower.models import Flower

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
import django
django.setup()
from userlog.models import UserLog
from routine.models import Routine
from routine.serializers import RoutineSerializer
from flower.models_process import FlowerMaker


class RoutineMaker:
    def __init__(self):
        pass

    def process(self, user_id):
        # Getting ALL of today logs
        today = datetime.now().date()
        all_today = list(UserLog.objects.filter(log_date__year=today.year,
                                                log_date__month=today.month,
                                                log_date__day=today.day,
                                                user_id=user_id).values())
        '''
            {
            'id': 6,
            'location': '비트캠프',
            'address': '서울 강남구 강남대로94길 20',
            'x': '127.029037792462',
            'y': '37.4994078625536',
            'log_date': datetime.datetime(2021, 12, 12, 17, 4, 1, 85772, tzinfo=<UTC>),
            'weather': '맑음',
            'log_type': 'study',
            'contents': '열심히 파이썬 개발 공부를 했다.',
            'user_id': 1
            }
        '''
        # Getting ALL of Routines
        all_routine = list(Routine.objects.filter(user_id=user_id).values())
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        # Checking log
        for log in all_today:
            flag = 0
            print(f'full_texts : {log["contents"]}')
            print('***** Checking log *****')
            log_id = log['id']
            location = log['location']
            day = days[log['log_date'].weekday()]
            time = log['log_date'].hour
            full_texts = log['contents']
            contents = []
            # cron = [0, 0, log['log_date'].hour, 0, 0, {days[log['log_date'].weekday()]: 1}]
            # grade = 0
            for i in Okt().pos(full_texts):
                if i[1] == 'Noun':
                    contents.append(i[0])
            print(f'log_id : {log_id}')
            print(f'location : {location}')
            print(f'day : {day}')
            print(f'time : {time}')
            # print(f'cron : {cron}')
            print(f'full_texts : {full_texts}')
            print(f'contents : {contents}')
            # Comparing Routine
            for routine in all_routine:
                grade = 0
                # Comparing Contents
                routine_contents = routine['contents'].split(' ')
                new_contents = []
                print(f' rotine_contents :: {routine_contents}')
                [[new_contents.append(lc) for rc in routine_contents if lc == rc] for lc in contents]
                print(f'new_contents :: {new_contents}')
                # 문장 간 유사도
                sentences = (full_texts, routine['contents'])
                tfidf_vectorizer = TfidfVectorizer()
                # 문장 벡터화 하기(사전 만들기)
                tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
                ### 코사인 유사도 ###
                # 첫 번째와 두 번째 문장 비교
                cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
                # 정규화 (두 점 사이의 거리 구하기)
                tfidf_normalized = tfidf_matrix / np.sum(tfidf_matrix)
                ### 맨하탄 유사도(격자로 된 거리에서의 최단거리) ###
                manhattan_d = manhattan_distances(tfidf_normalized[0:1], tfidf_normalized[1:2])
                if (manhattan_d > 0.7 or cos_similar > 0.7) and manhattan_d != 1:
                    grade += 2
                    # Comparing location
                    # [case 1] contents + location + cron
                    if location == routine['location']:
                        grade += 1
                        # grade = self.checking_cron(routine, day, grade, time, days, log)
                        # cron_time = int(routine['cron'][2])
                        # Comparing day
                        if routine['cron'][5].find(day) > -1:
                            grade += 1
                        # Comparing time
                        if time == int(routine['cron'][2]):
                            grade += 2
                        elif int(routine['cron'][2]) - 1 <= time <= int(routine['cron'][2]) + 1:
                            grade += 1
                        elif int(routine['cron'][2]) == 23:
                            if routine['cron'].find(days[log['log_date'].weekday() + 1]) > -1 and time == 0:
                                grade += 1
                        elif int(routine['cron'][2]) == 0:
                            if routine['cron'].find(days[log['log_date'].weekday() - 1]) > -1 and time == 23:
                                grade += 1
                        print('***** 변경 전 *****')
                        print(routine)
                        routine['grade'] += grade
                        routine['days'].append(day)
                        routine['hours'].append(time)
                        routine['log_id'].append(log_id)
                        routine['log_repeat'] = len(routine['log_id'])
                        print(f"routine['grade'] :: {routine['grade']}")
                        print(f"routine['log_repeat'] :: {routine['log_repeat']}")
                        routine['priority'] = routine['grade'] * routine['log_repeat']
                        routine['cron'][2] = max(routine['hours'], key=routine['hours'].count)
                        cron_day = []
                        for t in set(routine['days']):
                            if routine['days'].count(t) >= routine['days'].count(max(routine['days'], key=routine['days'].count)):
                                cron_day.append(t)
                        routine['cron'][5] = '.'.join(cron_day)
                        routine['log_id'] = list(set(routine['log_id']))
                        print('***** 변경 후 *****')
                        print(routine)
                        db = Routine.objects.get(id=routine['id'])
                        db.log_repeat = routine['log_repeat']
                        db.save()
                        db.priority = routine['priority']
                        db.save()
                        db.grade = routine['grade']
                        db.save()
                        db.cron = routine['cron']
                        db.save()
                        db.days = routine['days']
                        db.save()
                        db.hours = routine['hours']
                        db.save()
                        db.log_id = routine['log_id']
                        db.save()
                        flag = 1
                        # update Flower
                        try:
                            print("***** 111 update Flower")
                            print(f"****** routine_contents :: {routine_contents}")
                            print(f"' '.join(routine_contents) :: {' '.join(routine_contents)}")
                            get_flower = Flower.objects.get(title__iexact=' '.join(routine_contents))
                            print(f"****** get_flower :: {get_flower}")
                            FlowerMaker().update_flower(get_flower, log_id)
                            return "Update Flower"
                        except Flower.DoesNotExist:
                            FlowerMaker().create_flower(contents, log_id, user_id)
                            return "Update Flower"

            # new routine
            if flag == 0:
                Routine.objects.create(log_repeat=1,
                                       priority=0,
                                       grade=0,
                                       contents=' '.join(contents),
                                       location=location,
                                       cron=["0", "0", time, "0", "0", day],
                                       days=[day],
                                       hours=[time],
                                       log_id=[log_id],
                                       user_id=user_id
                                       )
                # new flower
                FlowerMaker().create_flower(contents, log_id, user_id)