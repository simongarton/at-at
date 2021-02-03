import json
import psycopg2
import requests
from api_key import api_key

shape_cache = {}


def setup_tables(conn):
    setup_vehicle(conn)


def setup_vehicle(conn):
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS vehicle')

    cursor.execute('''
        CREATE TABLE vehicle (
            id serial PRIMARY KEY,
            vehicle_id TEXT NOT NULL,
            latitude double precision NOT NULL,
            longitude double precision NOT NULL,
            speed double precision NOT NULL,
            bearing double precision NULL,
            timestamp bigint NOT NULL,
            label text NULL,
            license_plate text NULL,
            location geometry
        );
        ''')

    conn.commit()
    print('created vehicle table')


def got_vehicle(conn, vehicle_id):
    cursor = conn.cursor()
    sql = '''
        SELECT * FROM vehicle WHERE vehicle_id = %s;
        '''
    cursor.execute(sql, (vehicle_id,))
    vehicles = cursor.fetchall()
    return vehicles != None and len(vehicles) > 0


def load_vehicle(conn, vehicle):
    print(vehicle)

    # one-off load so no duplicates possible
    # if got_vehicle(conn, vehicle['id']):
    #    return False

    sql = '''
        INSERT INTO vehicle (vehicle_id, latitude, longitude, speed, bearing, timestamp, label, license_plate, location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID( ST_Point( %s, %s), 4326));
        '''

    vehicle_record = vehicle['vehicle']
    actual_vehicle = vehicle_record['vehicle']
    vehicle_position = vehicle_record['position']

    cursor = conn.cursor()
    cursor.execute(sql, (
        vehicle['id'],
        vehicle_position['latitude'],
        vehicle_position['longitude'],
        vehicle_position['speed'],
        vehicle_position['bearing'] if 'bearing' in vehicle_position else None,
        vehicle_record['timestamp'],
        actual_vehicle['label'] if 'label' in vehicle_position else None,
        actual_vehicle['license_plate'] if 'license_plate' in vehicle_position else None,
        vehicle_position['longitude'],
        vehicle_position['latitude'])
    )

    return True


def load_data(conn):
    url = 'https://api.at.govt.nz/v2/public/realtime/vehiclelocations'
    print('getting {}'.format(url))
    data = requests.get(url,
                        headers={'Ocp-Apim-Subscription-Key': api_key})
    if not data.status_code == 200:
        raise Exception('{} received from AT API : {}'.format(
            data.status_code, url))
    vehicles = data.json()['response']['entity']
    for vehicle in vehicles:
        if load_vehicle(conn, vehicle):
            print('loaded vehicle {} '.format(vehicle['id']))
        else:
            print('already got vehicle {} '.format(vehicle['id']))

    conn.commit()
    print('loaded {} vehicles'.format(len(vehicles)))


def empty_tables(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicle")
    conn.commit()
    print("vehicle table emptied")


def load_vehicles():
    conn = psycopg2.connect(dbname="at", user="at", password="at")

    # setup_tables(conn)

    empty_tables(conn)

    load_data(conn)


if __name__ == "__main__":
    load_vehicles()
