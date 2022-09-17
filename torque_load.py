from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from torque_sensor import TorqueSensor, TORQUE_DICTIONARY
from torque_config import MQTT_BROKER, SEND_TO_MQTT, MQTT_PORT, MQTT_PASSWORD, MQTT_USER, MQTT_TOPIC, LATITUDE_HOME, LONGITUDE_HOME, MY_TIMEZONE
from typing import List
from paho.mqtt import client as mqtt_client
import math
import pytz
from pytz import timezone
from datetime import datetime

class QueryData: 
    def __init__(self, key: str, data: str):
        self.key = key
        self.data = data


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # torque send a GET request.  All the values are passed are URL parameters
    def do_GET(self):
        parsed_path = urlparse(self.path)

        client = self._connect_mqtt()
        client.loop_start()

        if parsed_path.path.startswith("/upload"):
            self._send_ok_response()
            query_components = parse_qs(parsed_path.query)

            #Check if it's really data and not profile or first message with unit and name
            if "kc" not in query_components: #Engine RPM
                print("Pas de Data (RPM).  On ne considère pas les données")
            else:
                self._send_values_to_mqtt(client, query_components)
                self._send_distance_to_mqtt(client, query_components)

        client.disconnect()

    def _send_ok_response(self):
        self.send_response(200)
        self.end_headers()
        
        #Torque needs this response to continu to work properly
        self.wfile.write(b'OK!')

    def _send_values_to_mqtt(self, client, query_data):
        for data in query_data:
            if data in SEND_TO_MQTT:
                sensor: TorqueSensor = TORQUE_DICTIONARY[data]
                value = query_data[data][0]
                if data == 'time':
                    value = datetime.fromtimestamp(float(value) / 1000).astimezone(pytz.timezone(MY_TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')
                    print(value)

                topic = '{}/{}'.format(MQTT_TOPIC, sensor.field)
                self._publish_message_mqtt(client, topic, value)

    def _send_distance_to_mqtt(self, client, query_data):
        
        if 'distance_meter' in SEND_TO_MQTT and 'kff1005' in query_data and 'kff1006' in query_data:
            R = 6372800  # Earth radius in meters
    
            longitude = float(query_data['kff1005'][0])
            latitude = float(query_data['kff1006'][0])

            phi1, phi2 = math.radians(LATITUDE_HOME), math.radians(latitude) 
            dphi       = math.radians(latitude - LATITUDE_HOME)
            dlambda    = math.radians(longitude - LONGITUDE_HOME)
    
            a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
            distance = 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

            topic = '{}/{}'.format(MQTT_TOPIC, 'distance_meter')
            self._publish_message_mqtt(client, topic, round(distance))   


    def _connect_mqtt(self):

        client_id = 'torque_python'

        def on_connect(client, userdata, flags, rc):
            if rc != 0:
                print("Failed to connect to MQTT, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.on_connect = on_connect
        client.connect(MQTT_BROKER, MQTT_PORT)
        return client

    def _publish_message_mqtt(self, client, topic, message):
        result = client.publish(topic = topic, payload = message, retain = True)
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


print('Start http server on port 8011')
httpd = HTTPServer(('', 8011), SimpleHTTPRequestHandler)
httpd.serve_forever()