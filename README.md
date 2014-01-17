foodtrucks-backend
==================

These files are to be used with Google App Engine to serve as the backend for browsing food trucks in San Francisco.

The data pulled is from https://data.sfgov.org/Permitting/Mobile-Food-Facility-Permit/rqzj-sfat which shows what
food truck permits have been issued by the city of San Francisco.

The backend is to be used with abhayv/foodtrucks-frontend which uses Google Maps to display the location of
food trucks.

The API is as follows:
<pre>
HTTP GET /search
    Search for food truck locations given a query and a rectangular area defined by coordinates of the south west
    and north east corners:
    query: String to search for
    southWestLat: Latitude of the south west corner
    southWestLng: Longitude of the south west corner
    northEastLat: Latitude of the north east corner
    northEastLng: Longitude of the north east corner
    jsoncallback: Name of the JSONP callback function wrapper

    :return: JSONP encoded result in the following format:
    jsoncallback({'success': true, 'data': [
    <food_truck_data_1>,
    <food_truck_data_2>
    ]})

    Where food_truck_data is a JSON object with info fields described in http://data.sfgov.org/resource/rqzj-sfat.json

HTTP GET /build-index
    Fetches the data again from the source and rebuild the index
</pre>

Testing
-------

Open tests/SpecRunner.html in a browser or run using phantomjs
