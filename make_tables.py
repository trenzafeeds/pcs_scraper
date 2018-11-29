"""
Short tool for the included setup script to create the required
tables in your MySQL database.
"""

from peewee_lib import *

def main():

    results_database.connect()

    results_database.create_tables([Rider, Race, Result])

main()
