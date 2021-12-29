import os
import django
import csv
import sys

from common.models import ValueObject, Reader, Printer
from location.models import LocationData


class DbUploader:
    def __init__(self):
        vo = ValueObject()
        reader = Reader()
        self.printer = Printer()
        vo.context = 'location/data/'
        vo.fname = 'location_data.csv'
        self.csvfile = reader.new_file(vo)

    def insert_data(self):
        self.insert_location()

    def insert_location(self):
        with open(self.csvfile, newline='', encoding='utf8') as f:
            data_reader = csv.DictReader(f)
            # location,category,address
            for row in data_reader:
                # print(row)
                LocationData.objects.create(location=row['location'],
                                            category=row['category'],
                                            address=row['address'])
        print('LOCATION DATA UPLOADED SUCCESSFULLY!')

