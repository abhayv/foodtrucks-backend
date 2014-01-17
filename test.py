__author__ = 'abhay'

from nose.tools import *

import test_data
import search_index

class TestClass:
   def setUp(self):
      search_index.buildIndex(test_data.sample_food_trucks_data)

   def tearDown(self):
      pass

   def test_case_query_index(self):
      assert_equals(search_index.query_index, test_data.sample_query_index)

   def test_case_lat_index(self):
      assert_equals(search_index.sorted_latitudes, test_data.sample_latitude_index)

   def test_case_lng_index(self):
      assert_equals(search_index.sorted_longitudes, test_data.sample_longitude_index)

   def test_case_search_query(self):
      assert_equals(search_index.searchQuery('cold'), set([2, 3]))

   def test_case_search_query_case(self):
      assert_equals(search_index.searchQuery('Cold'), set([2, 3]))

   def test_case_search_find_le(self):
      assert_equals(search_index.find_le([10, 20, 30, 40], 20), 1)
      assert_equals(search_index.find_le([10, 20, 30, 40], 20.1), 1)
      assert_equals(search_index.find_le([10, 20, 30, 40], 30), 2)

   def test_case_search_find_ge(self):
      assert_equals(search_index.find_ge([10, 20, 30, 40], 20), 1)
      assert_equals(search_index.find_ge([10, 20, 30, 40], 30), 2)
      assert_equals(search_index.find_ge([10, 20, 30, 40], 20.1), 2)

   def test_case_search_lat(self):
      assert_equals(search_index.find_array_range_matching([10, 20, 30, 40], 20, 30), set([1, 2]))
      assert_equals(search_index.find_array_range_matching([10, 20, 30, 40], 19, 35), set([1, 2]))
      assert_equals(search_index.find_array_range_matching([10, 20, 30, 40], 9, 50), set([0, 1, 2, 3]))

   def test_case_search1(self):
       all_objectids = [x['objectid'] for x in search_index.all_results]
       results = search_index.search('', 37.7860914634251, -122.398658184604, 37.7901490737255, -122.3934729318)
       assert_equals([x['objectid'] for x in results],
                    all_objectids)

   def test_case_search2(self):
       all_objectids = [x['objectid'] for x in search_index.all_results[1:3]]
       results = search_index.search('', 37.7879000978181, -122.398658184604, 37.7901490737255, -122.394594036205)
       assert_equals([x['objectid'] for x in results],
                    all_objectids)

   def test_case_search3(self):
       all_objectids = [x['objectid'] for x in search_index.all_results[1:3]]
       results = search_index.search('', 37.787, -122.398658184604, 37.7901490737255, -122.394)
       assert_equals([x['objectid'] for x in results],
                    all_objectids)

   def test_case_search4(self):
       all_objectids = [x['objectid'] for x in search_index.all_results[2:4]]
       results = search_index.search('cold', 37.7860914634251, -122.398658184604, 37.7901490737255, -122.3934729318)
       assert_equals([x['objectid'] for x in results],
                    all_objectids)

   def test_case_search5(self):
       all_objectids = [x['objectid'] for x in search_index.all_results[1:2]]
       results = search_index.search('cheese', 37.7860914634251, -122.398658184604, 37.7901490737255, -122.3934729318)
       assert_equals([x['objectid'] for x in results],
                    all_objectids)


