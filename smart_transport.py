import requests
from math import fabs

CITY = "penza"


def get_zones(city=CITY):
    params = {
        "city": city
    }

    data = requests.get("https://58bus.ru/php/getZones.php?", params)
    if data:
        return data.json() if data.text != "Ошибка соединения: " else []


def get_rdata(rid=None, long0=0, lat0=0, long1=180, lat1=90, curk=0, city=CITY):
    rids = filter(lambda x: x, map(lambda x: x['routes_ids'] if "routes_ids" in x else '', get_zones(city)))
    params = {
        "city": city,
        "rids": ",".join(rids),
        "lng0": long0,
        "lat0": lat0,
        "lng1": long1,
        "lat1": lat1,
        "curk": curk
    }

    data = requests.get("https://58bus.ru/php/getVehiclesMarkers.php?", params)
    if data:
        data = data.json()['anims'] if data.text != "Ошибка соединения: " else []
        if data != [] and rid is not None:
            return data[list(map(lambda x: x['id'], data)).index(str(rid))] if str(rid) in map(lambda x: x['id'],
                                                                                               data) else []
        return data


def get_stations(city=CITY):
    params = {
        "city": city
    }
    data = requests.get("https://58bus.ru/php/getStations.php?", params)
    if data:
        data = data.json() if data.text != "Ошибка соединения: " else []
        for i in range(len(data)):
            data[i]['lat'] = data[i]['lat'] / 1000000
            data[i]['lng'] = data[i]['lng'] / 1000000
        return data


def get_station_forecasts(station_id, type=0, city=CITY):
    params = {
        "sid": station_id,
        "city": city,
        "type": type
    }

    data = requests.get("http://58bus.ru/php/getStationForecasts.php?", params)
    if data:
        return data.json() if data.text != "Ошибка соединения: " else []


def get_nearest_stop(long, lat, city=CITY):
    return min(get_stations(city), key=lambda x: fabs(x['lng'] - long)+fabs(x['lat'] - lat))


if __name__ == '__main__':
    from pprint import pprint
    import json
    data = get_rdata()
    json.dump(data, open('test.json', 'w'), ensure_ascii=False, indent=2)
    pprint(data)
