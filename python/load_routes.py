import json
import psycopg2
import requests
from api_key import api_key

shape_cache = {}


def setup_tables(conn):
    setup_route(conn)
    setup_trip(conn)


def setup_route(conn):
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS route')

    cursor.execute('''
        CREATE TABLE route (
            id serial PRIMARY KEY,
            route_id text NOT NULL,
            agency_id text NOT NULL,
            route_short_name text NOT NULL,
            route_long_name text NOT NULL,
            route_desc text NULL,
            route_type int NOT NULL,
            route_url text NULL,
            route_color text NULL,
            route_text_color text NULL,
            route geometry
        );
        ''')

    conn.commit()
    print('created route table')


def setup_trip(conn):
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS trip')

    cursor.execute('''
        CREATE TABLE trip (
            id serial PRIMARY KEY,
            route_id text NOT NULL,
            service_id text NOT NULL,
            trip_id text NOT NULL,
            trip_headsign text NOT NULL,
            direction_id int NOT NULL,
            block_id text NULL,
            shape_id text NOT NULL,
            trip_short_name text NULL,
            trip_type text NULL,
            route geometry
        );
        ''')

    conn.commit()
    print('created trip table')


def get_shape(shape_id):
    if shape_id in shape_cache:
        return shape_cache[shape_id]
    url = 'https://api.at.govt.nz/v2/gtfs/shapes/geometry/' + shape_id
    print('getting {}'.format(url))
    data = requests.get(url,
                        headers={'Ocp-Apim-Subscription-Key': api_key})
    if not data.status_code == 200:
        raise Exception('{} received from AT API : {}'.format(
            data.status_code, url))
    shapes = data.json()['response']
    if len(shapes) != 1:
        raise Exception('{} shapes in url {}'.format(len(shapes), url))
    shape = shapes[0]
    shape_cache[shape_id] = shape
    return shape


def load_trip(conn,  trip):
    shape = get_shape(trip['shape_id'])
    sql = '''
        INSERT INTO trip (route_id, service_id, trip_id, trip_headsign, direction_id, block_id, shape_id, trip_short_name, trip_type, route)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

    cursor = conn.cursor()
    cursor.execute(sql, (
        trip['route_id'],
        trip['service_id'],
        trip['trip_id'],
        trip['trip_headsign'],
        trip['direction_id'],
        trip['block_id'],
        trip['shape_id'],
        trip['trip_short_name'],
        trip['trip_type'],
        shape['the_geom'])
    )


def load_trips_for_route(conn,  route_id):
    url = 'https://api.at.govt.nz/v2/gtfs/trips/routeid/' + route_id
    print('getting {}'.format(url))
    data = requests.get(url,
                        headers={'Ocp-Apim-Subscription-Key': api_key})
    if not data.status_code == 200:
        raise Exception('{} received from AT API : {}'.format(
            data.status_code, url))
    trips = data.json()['response']
    for trip in trips:
        load_trip(conn, trip)


def load_route(conn, route):
    sql = '''
        INSERT INTO route (route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

    cursor = conn.cursor()
    cursor.execute(sql, (
        route['route_id'],
        route['agency_id'],
        route['route_short_name'],
        route['route_long_name'],
        route['route_desc'],
        route['route_type'],
        route['route_url'],
        route['route_color'],
        route['route_text_color'])
    )

    load_trips_for_route(conn, route['route_id'])
    conn.commit()


def load_data(conn):
    url = 'https://api.at.govt.nz/v2/gtfs/routes'
    print('getting {}'.format(url))
    data = requests.get(url,
                        headers={'Ocp-Apim-Subscription-Key': api_key})
    if not data.status_code == 200:
        raise Exception('{} received from AT API : {}'.format(
            data.status_code, url))
    routes = data.json()['response']
    for route in routes:
        load_route(conn, route)
        print('loaded route {} : {}'.format(
            route['route_short_name'], route['route_long_name']))
    conn.commit()
    print('loaded {} routes'.format(len(routes)))


def load_routes():
    conn = psycopg2.connect(dbname="at", user="at", password="at")

    setup_tables(conn)

    load_data(conn)


if __name__ == "__main__":
    print(api_key)
    load_routes()
