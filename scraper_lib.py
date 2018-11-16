"""
Function Library for a basic PCS results scraper
Kat Cannon-MacMartin
Marlboro College
10/10/18
"""
import datetime
import urllib2 as urlib
from bs4 import BeautifulSoup as bs

browser_spoof = {'User-agent' : 'Mozilla/5.0'}
base_rider_url = "https://www.procyclingstats.com/rider.php?id="
year_url_suffix = "&season="
current_year = datetime.datetime.now().year

class Row:

    def __init__(self, row_object):
        self.row_object = row_object
        self.elements_span = self.row_object.findChildren("span")
        if len(self.elements_span[1].contents) == 0:
            self.name = self.row_object.findChildren("a")[0].contents[0].contents[0]
            self.row_type = "tour_header"
            self.tour_name = self.name
            self.result = None
        else:
            for entry in self.elements_span:
                if len(entry.select("a[href*=race/]")) > 0:
                    a = entry.select("a[href*=race/]")[0].contents[0]
                    if isinstance(a, unicode) or isinstance(a, str):
                        self.name = a
                    else:
                        self.name = a.get_text()

            if self.name[-14:] == "Classification":
                self.row_type = "classification"
                self.tour_name = "unassigned"
            elif self.name[0:5] == "Stage" or self.name[0:8] == "Prologue":
                self.row_type = "stage"
                self.tour_name = "unassigned"
            else:
                self.row_type = "race"
                self.tour_name = None

            self.result = self.elements_span[1].contents[0]

            try:
                self.points_pcs = int(list(self.row_object.children)[-3].contents[0])
            except:
                self.points_pcs = 0
                

class Sheet:

    def __init__(self, soup, rider, year):
        self.soup = soup
        self.rider = rider
        self.year = year
        self.rows_raw = self.soup.find_all("div", class_ = "row")
        self.rows = []
        self.points_rows = 0.0
        index = 0
        tour_name_holder = "unassigned"
        while index < len(self.rows_raw):
            row_holder = Row(self.rows_raw[index])
            if row_holder.row_type == "tour_header":
                tour_name_holder = row_holder.name
            else:
                self.points_rows += 1
            if row_holder.row_type in ["stage", "classification"]:
                row_holder.tour_name = tour_name_holder
            self.rows.append(row_holder)
            index += 1
            
    def get_pcs_points(self, method="sum"):
        if method not in ("sum", "avg"):
            raise ValueError("Supported method entries are 'sum' or 'avg'")
        ret_points = 0
        for row in self.rows:
            if row.row_type != "tour_header":
                ret_points += row.points_pcs
        if method == "avg":
            ret_points = float(ret_points) / self.points_rows
        return ret_points

class Rider:

    def __init__(self, url_id):
        self.url_id = url_id
        self.base_url = base_rider_url + str(url_id)
        
        self.base_page_soup = bs(urlib.urlopen(urlib.Request(self.base_url, headers = browser_spoof)).read(), 'html.parser')
        self.name = str(self.base_page_soup.find_all("title")[0].contents[0])
        self.sheets = {current_year:Sheet(self.base_page_soup, self.name, current_year)}
        
    def load_sheets(self, start_year, end_year):
        for year in xrange(start_year, end_year+1):
            self.sheets[year] = Sheet(bs(urlib.urlopen(urlib.Request(self.base_url+year_url_suffix+str(year), headers = browser_spoof)).read(), 'html.parser'), self.name, year)

