__author__ = 'abhay'

# Sample data downloaded for testing
sample_food_trucks_data = [
  {
    "location":{
      "needs_recoding":False,
      "longitude":"-122.398658184594",
      "latitude":"37.7901490874965"
    },
    "status":"REQUESTED",
    "expirationdate":"2013-03-15T00:00:00",
    "permit":"13MFF-0068",
    "block":"3708",
    "received":"Mar 14 2013  3:34PM",
    "facilitytype":"Truck",
    "blocklot":"3708055",
    "locationdescription":"01ST ST: STEVENSON ST to JESSIE ST (21 - 56)",
    "cnn":"101000",
    "priorpermit":"0",
    "schedule":"http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=13MFF-0068&ExportPDF=1&Filename=13MFF-0068_schedule.pdf",
    "address":"50 01ST ST",
    "applicant":"Cupkates Bakery, LLC",
    "lot":"055",
    "fooditems":"Cupcakes",
    "longitude":"-122.398658184604",
    "latitude":"37.7901490737255",
    "objectid":"427856",
    "y":"2115738.283",
    "x":"6013063.33"
  }
  ,
  {
    "location":{
      "needs_recoding":False,
      "longitude":"-122.395881037809",
      "latitude":"37.7891192216837"
    },
    "status":"APPROVED",
    "expirationdate":"2014-03-15T00:00:00",
    "permit":"13MFF-0060",
    "block":"3720",
    "received":"Mar 14 2013 12:50PM",
    "facilitytype":"Truck",
    "blocklot":"3720008",
    "locationdescription":"01ST ST: NATOMA ST to HOWARD ST (165 - 199)",
    "cnn":"106000",
    "priorpermit":"0",
    "approved":"2013-06-06T17:05:20",
    "schedule":"http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=13MFF-0060&ExportPDF=1&Filename=13MFF-0060_schedule.pdf",
    "address":"400 HOWARD ST",
    "applicant":"Cheese Gone Wild",
    "lot":"008",
    "fooditems":"Grilled Cheese Sandwiches",
    "longitude":"-122.395881037818",
    "latitude":"37.7891192079118",
    "objectid":"427795",
    "y":"2115347.095",
    "x":"6013858.06"
  }
  ,
  {
    "location":{
      "needs_recoding":False,
      "longitude":"-122.394594036195",
      "latitude":"37.7879001115912"
    },
    "status":"APPROVED",
    "expirationdate":"2014-03-15T00:00:00",
    "permit":"13MFF-0063",
    "block":"3737",
    "received":"Mar 14 2013  2:35PM",
    "facilitytype":"Truck",
    "blocklot":"3737012",
    "locationdescription":"01ST ST: CLEMENTINA ST to FOLSOM ST (245 - 299)",
    "cnn":"110000",
    "priorpermit":"1",
    "approved":"2013-03-19T14:01:19",
    "schedule":"http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=13MFF-0063&ExportPDF=1&Filename=13MFF-0063_schedule.pdf",
    "address":"245 01ST ST",
    "applicant":"Mini Mobile Food Catering",
    "lot":"012",
    "fooditems":"Cold Truck: Corn Dogs: Noodle Soups: Candy: Pre-packaged Snacks: Sandwiches: Chips: Coffee: Tea: Various Beverages",
    "longitude":"-122.394594036205",
    "latitude":"37.7879000978181",
    "objectid":"427837",
    "y":"2114895.75",
    "x":"6014220.898"
  }
  ,
  {
    "location":{
      "needs_recoding":False,
      "longitude":"-122.39347293179",
      "latitude":"37.7860914772"
    },
    "status":"APPROVED",
    "expirationdate":"2014-03-15T00:00:00",
    "permit":"13MFF-0104",
    "block":"3749",
    "received":"Apr 18 2013  9:15AM",
    "facilitytype":"Truck",
    "blocklot":"3749058",
    "locationdescription":"01ST ST: LANSING ST to HARRISON ST \\ I-80 E ON RAMP (362 - 399)",
    "cnn":"113000",
    "priorpermit":"1",
    "approved":"2013-06-11T13:06:30",
    "schedule":"http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=13MFF-0104&ExportPDF=1&Filename=13MFF-0104_schedule.pdf",
    "address":"390 01ST ST",
    "applicant":"Steve's Mobile Deli",
    "lot":"058",
    "fooditems":"Cold Truck: Pre-packaged sandwiches: Burgers: Hot Dogs: Muffin Sandwiches: Enchiladas: Bagels: Burritos: Salads: Snacks: Beverages",
    "longitude":"-122.3934729318",
    "latitude":"37.7860914634251",
    "objectid":"438423",
    "y":"2114230.765",
    "x":"6014531.475"
  }
]

sample_query_index = {'mini': set([2]), 'cheese': set([1]), 'muffin': set([3]), 'llc': set([0]), 'cold': set([2, 3]),
                      'gone': set([1]), 'cupcakes': set([0]), 'cupkates': set([0]), 'truck:': set([2, 3]),
                      'deli': set([3]), 'hot': set([3]), 'various': set([2]), 'sandwiches': set([1]),
                      'grilled': set([1]), 'pre-packaged': set([2, 3]), 'candy:': set([2]), 'tea:': set([2]),
                      'beverages': set([2, 3]), 'food': set([2]), 'corn': set([2]), 'chips:': set([2]),
                      'sandwiches:': set([2, 3]), 'catering': set([2]), 'burgers:': set([3]), 'wild': set([1]),
                      'dogs:': set([2, 3]), 'bagels:': set([3]), 'noodle': set([2]), 'enchiladas:': set([3]),
                      'mobile': set([2, 3]), 'coffee:': set([2]), 'salads:': set([3]), 'bakery,': set([0]),
                      'soups:': set([2]), "steve's": set([3]), 'burritos:': set([3]), 'snacks:': set([2, 3])}
sample_latitude_index = [37.7860914634251, 37.7879000978181, 37.7891192079118, 37.7901490737255]
sample_longitude_index = [-122.398658184604, -122.395881037818, -122.394594036205, -122.3934729318]

