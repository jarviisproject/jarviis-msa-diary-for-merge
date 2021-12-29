import schedule
import time

from routine.models_process import RoutineMaker
from userlog.models_data import DbUploader


class JarviisSchedule:
    def __init__(self):
        pass

    def process(self):
        # TEST
        # schedule.every(5).seconds.do(j.test)
        # Routine Schedule
        schedule.every().day.at("05:00").do(self.make_routine())
        # Log Schedule
        schedule.every().day.at("09:00").do(self.make_log())
        schedule.every().day.at("11:40").do(self.make_log())
        schedule.every().day.at("15:20").do(self.make_log())
        schedule.every().day.at("18:15").do(self.make_log())
        schedule.every().day.at("21:55").do(self.make_log())
        while True:
            schedule.run_pending()

    def make_log(self):
        DbUploader().insert_data()

    def make_routine(self):
        RoutineMaker().process(1)

    def test(self):
        print("*"*100)
        print("test 출력")


if __name__ == '__main__':
    j = JarviisSchedule()
    j.process()


