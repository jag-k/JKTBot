import requests


def get_rdata(rid=None):
    data = requests.get("https://58bus.ru/php/getVehiclesMarkers.php?"
                        "rids=137-0,138-0,12-0,11-0,140-0,139-0,144-0,143-0,3-0,4-0,198-0,"
                        "197-0,113-0,114-0,115-0,116-0,142-0,141-0,91-0,92-0,13-0,"
                        "14-0,6-0,5-0,146-0,145-0,16-0,15-0,148-0,147-0,167-0,168-0,"
                        "136-0,135-0,17-0,18-0,176-0,175-0,152-0,153-0,155-0,154-0,"
                        "150-0,151-0,230-0,231-0,118-0,117-0,166-0,165-0,93-0,94-0,"
                        "120-0,119-0,178-0,177-0,164-0,285-0,238-0,239-0,232-0,233-0,"
                        "180-0,179-0,182-0,181-0,35-0,36-0,121-0,122-0,124-0,123-0,"
                        "227-0,226-0,95-0,96-0,416-0,417-0,236-0,237-0,184-0,183-0,229-0,"
                        "228-0,252-0,251-0,109-0,110-0,186-0,185-0,188-0,187-0,189-0,190-0,"
                        "104-0,103-0,163-0,162-0,105-0,106-0,102-0,101-0,243-0,244-0,88-0,89-0,"
                        "161-0,160-0,98-0,97-0,126-0,125-0,29-0,30-0,158-0,159-0,99-0,100-0,235-0,"
                        "234-0,112-0,111-0,157-0,156-0,81-0,82-0"
                        "&lat0=0&lng0=0&lat1=90&lng1=180&curk=0&city=penza")
    if data:
        data = data.json()['anims'] if data.text != "Ошибка соединения: " else []
        return data[list(map(lambda x: x['id'], data)).index(str(rid))] if data != [] and rid is not None and \
                                                                           str(rid) in map(lambda x: x['id'], data) \
            else data


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
