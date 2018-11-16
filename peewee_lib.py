"""
Library for MySQL interfacing with pcs_scraper
"""

from peewee import *
from mysql_login_info import *

results_database = MySQLDatabase(mysql_db_name, user=mysql_uname, password=mysql_pw, host='localhost')

class BaseModel(Model):
    class Meta:
        database = results_database

class Rider(BaseModel):

    id = IntegerField()
    name = CharField()
    birthday = DateField()
    current_age = IntegerField()

class Race(BaseModel):

    name = CharField()
    pcs_name = CharField()
    
class Result(BaseModel):

    name = CharField()
    year = IntegerField()
    date = DateField()
    
    position = Integerfield()
    points_pcs = IntegerField()

    race = ForeignKeyField(Race, backref='results')
    rider = ForeignKeyField(Rider, backref'results')

    
    
