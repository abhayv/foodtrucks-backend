__author__ = 'abhay'

import collections
import bisect
import logging

query_index = collections.defaultdict(set)
latitude_index = []
latitude_index_to_result_index = {}
longitude_index = []
longitude_index_to_result_index = {}
all_results = []

def buildIndex(results):
    global all_results
    global latitude_index
    global longitude_index
    global query_index
    global latitude_index_to_result_index
    global longitude_index_to_result_index
    all_results = results
    latitude_index = []
    longitude_index = []
    latitude_index_to_result_index = {}
    longitude_index_to_result_index = {}
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
        insert_lat = bisect.bisect_right(latitude_index, lat)
        latitude_index.insert(insert_lat, lat)
        latitude_index_to_result_index[insert_lat] = i

        insert_lng = bisect.bisect_right(longitude_index, lng)
        longitude_index.insert(insert_lng, lng)
        longitude_index_to_result_index[insert_lng] = i

    logging.info("query_index %s" % query_index)
    logging.info("latitude_index %s" % latitude_index)
    logging.info("longitude_index %s" % longitude_index)
    logging.info("latitude_index_to_result %s" % latitude_index_to_result_index)
    logging.info("longitude_index_to_result %s" % longitude_index_to_result_index)

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

def latLongQuery(array, value_min, value_max):
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
    lat_matches = latLongQuery(latitude_index, southWestLat, northEastLat)
    # Convert to result indices
    lat_matches = set([latitude_index_to_result_index[x] for x in lat_matches])
    lng_matches = latLongQuery(longitude_index, southWestLng, northEastLng)
    # Convert to result indices
    lng_matches = set([longitude_index_to_result_index[x] for x in lng_matches])
    if query:
        query_matches = searchQuery(query)
        matches = set.intersection(lat_matches, lng_matches, query_matches)
    else:
        matches = set.intersection(lat_matches, lng_matches)
    logging.info("search %s" % locals())
    return [all_results[i] for i in range(len(all_results)) if i in matches]