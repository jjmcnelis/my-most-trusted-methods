from math import radians, cos, sin, asin, sqrt


def haversine_distance(lon1: float, lat1: float, lon2: float, lat2: float, a: float=6378137.):
    """https://en.wikipedia.org/wiki/Haversine_formula
    :param lon1: Longitude of the first xy coordinate pair
    :param lat1: Latitude of the first xy coordinate pair
    :param lon2: Longitude of the second xy coordinate pair
    :param lat2: Latitude of the second xy coordinate pair
    :param a: Equatorial radius of reference ellipse (meters)
    :returns: Great circle distance between input lon, lat pairs (meters)
    """
    lon1, lon2 = radians(lon1), radians(lon2)
    lat1, lat2 = radians(lat1), radians(lat2)
    haversine = sin((lat2-lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2-lon1)/2)**2
    ihaversine = 2 * asin(sqrt(haversine))
    return(ihaversine * a)


def geojson_linestring_feature_collection(longitudes: list, latitudes: list, **kwargs):
    return {
		"type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [list(c) for c in zip(longitudes, latitudes)]
                },
                "properties": kwargs
            }
        ]
    }
