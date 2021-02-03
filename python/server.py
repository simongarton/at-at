import flask
import psycopg2

conn = None

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>AT-AT</h1><p>Auckland Transport API Test</p>"


def build_vehicle(record):
    return {
        'id': record[0],
        'latitude': record[1],
        'longitude': record[2],
        'speed': record[3],
        'bearing': record[4],
        'timestamp': record[5],
        'label': record[6],
        'license_plate': record[7],
        'easting': record[8],
        'northing': record[9],
    }


@app.route('/vehicles', methods=['GET'])
def vehicles():
    global conn
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT vehicle_id, latitude, longitude, speed, bearing, timestamp, label, license_plate, 
        public.st_x(public.ST_Transform(location, 2193)) AS easting,
        public.st_y(public.ST_Transform(location, 2193)) AS northing
        FROM vehicle
        ''')
    records = cursor.fetchall()

    vehicles = [build_vehicle(record) for record in records]
    return {'vehicles': vehicles}


def run_server():
    global conn
    conn = psycopg2.connect(dbname="at", user="at", password="at")
    app.run()


if __name__ == "__main__":
    run_server()
