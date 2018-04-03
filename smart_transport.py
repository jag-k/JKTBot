import requests


def get_zones(city="penza"):
    params = {
        "city": city
    }

    data = requests.get("https://58bus.ru/php/getZones.php?", params)
    if data:
        return data.json() if data.text != "Ошибка соединения: " else []


def get_rdata(rid=None, long0=0, lat0=0, long1=180, lat1=90, curk=0, city="penza"):
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


def get_stations(city="penza"):
    params = {
        "city": city
    }
    data = requests.get("https://58bus.ru/php/getStations.php?", params)
    if data:
        return data.json() if data.text != "Ошибка соединения: " else []


def get_station_forecasts(station_id, type=0, city="penza"):
    params = {
        "sid": station_id,
        "city": city,
        "type": type
    }

    data = requests.get("http://58bus.ru/php/getStationForecasts.php?", params)
    if data:
        return data.json() if data.text != "Ошибка соединения: " else []


if __name__ == '__main__':
    from pprint import pprint
    import json
    data = get_rdata()
    json.dump(data, open('test.json', 'w'), ensure_ascii=False, indent=2)
    pprint(data)
