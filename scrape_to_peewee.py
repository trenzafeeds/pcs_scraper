import scraper_lib as pylib
import peewee_lib as pw

class Rider_bind:

    def __init__(self, rider_id):

        self.rider_py = pylib.Rider(rider_id)
        self.rider_pw = pw.Rider(pcsid=self.rider_py.url_id, name=self.rider_py.name)
	self.rider_pw.save()

