import scraper_lib as pylib
import peewee_lib as pw

from unidecode import unidecode

class Sheet_bind:

    def __init__(self, rider_obj, sheet):

        self.year = sheet.year
        self.rider = sheet.rider
        self.rows = []
        
        for row in sheet.rows:
            
            if row.row_type == "tour_header":
                pass
            else:
                temp_query = pw.Race.select().where(pw.Race.name == unidecode(row.race))
                if not temp_query.exists():
                    temp_query = pw.Race(name=unidecode(row.race))
                    temp_query.save()
                else:
                    temp_query = temp_query.get()
            
                temp_res = pw.Result(name=unidecode(row.name),\
                                     year=sheet.year,\
                                     points_pcs=row.points_pcs)
                                  
                                  
                
                if row.row_type in ["stage", "classification"]:
                    temp_res.name = unidecode(row.race) + ' ' + unidecode(row.name)

                if row.result == "DNF":
                    temp_res.position = 0
                else:
                    temp_res.position = row.result
                    
                temp_res.race=temp_query
                temp_res.rider=rider_obj
                temp_res.save()
            temp_query = None
            temp_res = None
            

class Rider_bind:

    def __init__(self, rider_id):

        self.rider_py = pylib.Rider(rider_id)
        self.rider_pw = pw.Rider(pcsid=self.rider_py.url_id, name=unidecode(self.rider_py.name))
	self.rider_pw.save()
        
        
    def load_sheets(self, start_year, end_year):

        for year in xrange(start_year, end_year + 1):
            if year not in self.rider_py.sheets:
                self.rider_py.load_sheets(year, year)
            
            loaded_sheet = Sheet_bind(self.rider_pw, self.rider_py.sheets[year]) 
        
def main():
    pw.results_database.connect()

main()
