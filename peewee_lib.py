"""
Library for MySQL interfacing with pcs_scraper
"""

from peewee import *
from mysql_login_info import *

results_database = MySQLDatabase(mysql_db_name, user=mysql_uname, password=mysql_pw, host='localhost')

class BaseModel(Model):
    class Meta:
        database = results_database

class Rider_PW(BaseModel):

    pcsid = IntegerField()
    name = CharField()

class Race_PW(BaseModel):

    name = CharField()
    pcs_name = CharField()
    
class Result_PW(BaseModel):

    name = CharField()
    year = IntegerField()
    date = DateField()
    
    position = Integerfield()
    points_pcs = IntegerField()

    race = ForeignKeyField(Race_PW, backref='results')
    rider = ForeignKeyField(Rider_PW, backref='results')

    
    
