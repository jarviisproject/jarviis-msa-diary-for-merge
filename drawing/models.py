from datetime import datetime

from django.db import models

# Create your models here.
from common.models import ValueObject
from drawing.models_draw import QuickDrawData, QuickDrawDataGroup
from drawing.models_merge import MergeImg


class Drawing:
    def __init__(self, vo):
        self.vo = vo

    def process(self, topic):
        qd = QuickDrawData()
        path = self.vo.context
        [qd.get_drawing(topic[i]).image.save(f"{path}/test{i}.gif")for i in range(len(topic))]
        return MergeImg(self.vo).process(len(topic))
