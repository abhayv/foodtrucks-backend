__author__ = 'abhay'

import collections
import bisect
import logging

query_index = collections.defaultdict(set)
sorted_latitudes = []
latitude_to_result_index = collections.defaultdict(set)
sorted_longitudes = []
longitude_to_result_index = collections.defaultdict(set)
all_results = []

def buildIndex(results):
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
            logging.info("Result with no lat %s" % result)
            continue
        lat = float(lat)
        lng = result.get('longitude')
        if not lng:
            logging.info("Result with no lng %s" % result)
            continue
        lng = float(lng)
        bisect.insort_right(sorted_latitudes, lat)
        bisect.insort_right(sorted_longitudes, lng)

        latitude_to_result_index[lat].add(i)
        longitude_to_result_index[lng].add(i)

    logging.info("query_index %s" % query_index)
    logging.info("sorted_latitudes %s" % sorted_latitudes)
    logging.info("sorted_longitudes %s" % sorted_longitudes)
    logging.info("latitude_index_to_result %s" % latitude_to_result_index)
    logging.info("longitude_index_to_result %s" % longitude_to_result_index)

def searchQuery(query):
    if query == '':
        to_ret = set(range(len(all_results)))
        logging.info("returning all %s %s" % (to_ret, len(all_results)))
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
    logging.info("find_ge %s" % locals())
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
        minv = find_ge(array, value_min)
        logging.info("latLongQuery1 %s" % locals())
        maxv = find_le(array, value_max)
        logging.info("latLongQuery2 %s" % locals())
        return set(range(minv, maxv + 1))
    except ValueError:
        logging.info("not found %s" % locals())
    return set()

def search(query, southWestLat, southWestLng, northEastLat, northEastLng):
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
    logging.info("search %s" % locals())
    return [all_results[i] for i in range(len(all_results)) if i in matches]