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
    rids = list(filter(lambda x: x, map(lambda x: x['routes_ids'] if "routes_ids" in x else '', get_zones(city))))
    params = {
        "city": city,
        "rids": ",".join(",".join(i) for i in rids),
        "lng0": long0,
        "lat0": lat0,
        "lng1": long1,
        "lat1": lat1,
        "curk": curk
    }

    data = requests.get("https://58bus.ru/php/getVehiclesMarkers.php?", params)
    if data:
        data = data.json()['anims'] if data.text != "Ошибка соединения: " and 'anims' in data.json() else []
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


def get_gos_num(driver_id):
    drivers_data = get_rdata(driver_id)
    return drivers_data["gos_num"] if "gos_num" in drivers_data else "Гос. номер не найден"


def string_arrival_time(arrt, minus=10):
    return ("~%s мин." % (arrt // 60)) if arrt >= 60 else ("меньше минуты…" if arrt <= minus else "почти на месте…")


def station_filter(station_data: list, sorted_key=(lambda x: x)):
    data = {
        "М": {},
        "Т": {},
        "А": {},
    }
    new_data = []
    for i in range(len(station_data)):
        station = station_data[i]
        if station['rnum'] in data[station['rtype']]:
            arrt, index = data[station['rtype']][station['rnum']]
            if arrt > station['arrt']:
                new_data[new_data.index(station_data[index])] = station
                data[station['rtype']][station['rnum']] = station['arrt'], i
        else:
            data[station['rtype']][station['rnum']] = station['arrt'], i
            new_data.append(station)

    return sorted(new_data, key=sorted_key)

