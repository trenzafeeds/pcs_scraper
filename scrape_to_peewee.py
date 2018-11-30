import scraper_lib as pylib
import peewee_lib as pw

class Sheet_bind:

    def __init__(self, rider_obj, sheet):

        self.year = sheet.year
        self.rider = sheet.rider
        self.rows = []
        
        for row in sheet.rows:
            
            if row.row_type == "tour_header":
                pass
            else:
                temp_query = pw.Race.select().where(pw.Race.name == row.race)
                if not temp_query.exists():
                    temp_query = pw.Race(name=row.race)
                    temp_query.save()
                else:
                    pass
            
                temp_res = pw.Result(name=(row.race + ' ' + row.name),\
                                  year=sheet.year,\
                                  position=row.result,\
                                  points_pcs=row.points_pcs,\
                                  race=temp_query,\
                                  rider=rider_obj)
                
                if row.row_type in ["stage", "classification"]:
                    temp_res.name = row.race + ' ' + row.name

                temp_res.save()
            temp_query = None
            temp_res = None
            

class Rider_bind:

    def __init__(self, rider_id):

        self.rider_py = pylib.Rider(rider_id)
        self.rider_pw = pw.Rider(pcsid=self.rider_py.url_id, name=self.rider_py.name)
	self.rider_pw.save()
        
        
    def load_sheets(self, start_year, end_year):

        for year in xrange(start_year, end_year + 1):
            if year not in self.rider_py.sheets:
                self.rider_py.load_sheets(year, year)
            
            loaded_sheet = Sheet_bind(self, self.rider_py.sheets[year])
            loaded_sheet.save() 
                

        
def main():
    pw.results_database.connect()

main()
