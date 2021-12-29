from userlog.models import UserLog
from userlog.models_process import LogData


class DbUploader:
    def __init__(self):
        pass

    def insert_data(self):
        self.insert_userlog('1')

    def insert_userlog(self, user_id):
        data = LogData().process()
        UserLog.objects.create(location=data['location'],
                               address=data['address'],
                               x=data['x'],
                               y=data['y'],
                               weather=data['weather'],
                               log_type=data['log_type'],
                               contents=data['contents'],
                               # item=data['item'],
                               user_id=user_id)
        print('LOG DATA UPLOADED SUCCESSFULY!')

