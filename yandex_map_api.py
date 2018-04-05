from pprint import pprint
from multitool import *


def get_coord(location, sco='longlat'):
    params = {
        "geocode": location,
        "sco": sco
    }
    response = get_request(GEOCODE, params)
    if response:
        res = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return tuple(map(float, res.split()))


def search_spn(geo_object):
    if type(geo_object) is not dict:
        geo_object = get_geo_object(*geo_object)
    data = geo_object["boundedBy"]["Envelope"]
    upper = tuple(map(float, data["upperCorner"].split()))
    lower = tuple(map(float, data["lowerCorner"].split()))
    return upper[0] - lower[0], upper[1] - lower[1]


def get_geo_object(long, lat):
    params = {
        "geocode": str_param(long, lat)
    }

    res = get_request(GEOCODE, params).json()
    geo_object = res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return geo_object


def get_address(coords, postal_code=False):
    geo_object = get_geo_object(coords[0], coords[1])["metaDataProperty"]["GeocoderMetaData"]
    address = geo_object["text"]
    if postal_code and "Address" in geo_object and 'postal_code' in geo_object["Address"]:
        address += ", " + geo_object["Address"]['postal_code']
    return address


def create_point(long, lat, style='pm2', color='wt', size='m', content=''):
    """
    https://tech.yandex.ru/maps/doc/staticapi/1.x/dg/concepts/markers-docpage/
    :return: point data
    """
    return str_param(long, lat, ''.join((style, color, size, content)))
