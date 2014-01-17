# Copyright (C) 2014 Abhay Vardhan. All Rights Reserved.
"""
Author: abhay.vardhan@gmail.com

Utility functions to keep a search index for queries, latitudes and longitudes.
Ideally we would use a geospatial search but instead we look into a rectangular area
given by the south west corner and the north east corner.
"""

__author__ = 'abhay'

import collections
import bisect
import logging
import urllib2
import json

# We should store the variables below in some persistent store and refresh only as needed.
# However, for the sake of demonstration, we are currently storing this in memory and preserving across
# HTTP requests

# Array of all the results. All the other variables will store this array's indices
all_results = []

# This is an index of all words in food truck metadata text. Each entry is a set of result indices that have that word
query_index = collections.defaultdict(set)

# Array of latitudes occurring in the results, sorted in ascending order
sorted_latitudes = []

# Dictionary converting a given latitude to a set of result indices that have that latitude
latitude_to_result_index = collections.defaultdict(set)

# Array of longitiudes occurring in the results, sorted in ascending order
sorted_longitudes = []

# Dictionary converting a given longitude to a set of result indices that have that longitude
longitude_to_result_index = collections.defaultdict(set)

FOOD_DATA_URL = 'http://data.sfgov.org/resource/rqzj-sfat.json'
def build():
    """
    Fetch the json data and build the indexes
    :return:
    """
    response = urllib2.urlopen(FOOD_DATA_URL)
    raw = response.read()
    results = json.loads(raw)
    logging.debug("results %s" % results)
    buildIndex(results)

def buildIndex(results):
    """
    Build the various indexes. The plan is as follows:
    Process each item in the result and extract all interesting words, latitude, and longitude from the result.
    The interesting words are put in the query_index.
    The latitudes and longitudes are sorted. Later when a query for a rectangular area comes, we will use these to find
    the matching latitudes and longitudes in the range of the rectangle.
    :param results:
    :return:
    """
    global all_results
    global sorted_latitudes
    global sorted_longitudes
    global query_index
    global latitude_to_result_index
    global longitude_to_result_index
    all_results = results
    sorted_latitudes = []
    sorted_longitudes = []
    latitude_to_result_index = collections.defaultdict(set)
    longitude_to_result_index = collections.defaultdict(set)
    query_index = collections.defaultdict(set)

    for i, result in enumerate(results):
        for word in result['applicant'].split() + result['fooditems'].split():
            query_index[word.lower()].add(i)
        lat = result.get('latitude')
        if not lat:
            logging.debug("Result with no lat %s" % result)
            continue
        lat = float(lat)
        lng = result.get('longitude')
        if not lng:
            logging.debug("Result with no lng %s" % result)
            continue
        lng = float(lng)
        bisect.insort_right(sorted_latitudes, lat)
        bisect.insort_right(sorted_longitudes, lng)

        latitude_to_result_index[lat].add(i)
        longitude_to_result_index[lng].add(i)

    logging.debug("query_index %s" % query_index)
    logging.debug("sorted_latitudes %s" % sorted_latitudes)
    logging.debug("sorted_longitudes %s" % sorted_longitudes)
    logging.debug("latitude_index_to_result %s" % latitude_to_result_index)
    logging.debug("longitude_index_to_result %s" % longitude_to_result_index)


def searchQuery(query):
    """
    Find result indices matching a query
    :param query:
    :return:
    """
    if query == '':
        to_ret = set(range(len(all_results)))
        return to_ret
    tokens = query.split()
    matches = []
    # We could do more efficient matching with sorted hit lists but we just use sets for now.
    for token in tokens:
        matches.append(query_index.get(token.lower(), set()))
    return set.intersection(*matches)


def find_le(a, x):
    'Find rightmost value index less than or equal to x'
    i = bisect.bisect_right(a, x)
    if i:
        return i - 1
    raise ValueError


def find_ge(a, x):
    'Find leftmost item index greater than or equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a):
        return i
    raise ValueError


def find_array_range_matching(array, value_min, value_max):
    """
    Search for locations in the array
    :param array:
    :param value:
    :return: set of indices that match
    """
    try:
        mini = find_ge(array, value_min)
        maxi = find_le(array, value_max)
        return set(range(mini, maxi + 1))
    except ValueError:
        logging.info("not found %s %s" % (value_min, value_max))
    return set()


def search(query, southWestLat, southWestLng, northEastLat, northEastLng):
    """
    Main search function.
    Compute:
    a) The result indices matching query terms
    b) Latitude matches in the rectangle defined by input parameters. Convert the latitudes to result indices
    c) Longitude matches in the rectangle defined by input parameters. Convert the Longitude to result indices
    d) Intersect all the sets of result indices
    e) Pull the actual results using the result indices
    :param query:
    :param southWestLat:
    :param southWestLng:
    :param northEastLat:
    :param northEastLng:
    :return:
    """
    if not all_results:
        build()
    lat_matches = find_array_range_matching(sorted_latitudes, southWestLat, northEastLat)
    # Convert to result indices
    result_matches_by_lat = set()
    for x in lat_matches:
        result_indices = latitude_to_result_index[sorted_latitudes[x]]
        result_matches_by_lat = result_matches_by_lat.union(result_indices)

    lng_matches = find_array_range_matching(sorted_longitudes, southWestLng, northEastLng)
    # Convert to result indices
    result_matches_by_lng = set()
    for x in lng_matches:
        result_indices = longitude_to_result_index[sorted_longitudes[x]]
        result_matches_by_lng = result_matches_by_lng.union(result_indices)
    if query:
        query_matches = searchQuery(query)
        matches = set.intersection(result_matches_by_lat, result_matches_by_lng, query_matches)
    else:
        matches = set.intersection(result_matches_by_lat, result_matches_by_lng)
    return [all_results[i] for i in range(len(all_results)) if i in matches]