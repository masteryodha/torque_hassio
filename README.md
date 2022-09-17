# Description

This project is intended to be a way to get the information from the fuel left on my car to home assistant.
I could then be able to add a dashboard or notification based on fuel level.

To make this possible I used an OBD2 device to read the different sensors of my car and with the Torque App, I can send this information to a custom web server that will be able to transfert the required information to MQTT.

From MQTT, home assistant can get the different attribute and integrate it in its dashbord or automation.


# Special Note about this project
I also purchased an OBD2 cable extension with a ON/OFF switch for my car.  I was afraid that if I didn't use my car from a long time with OBD2 connected that it will drain my battery.
So be aware of that.
There seems to be OBD2 device that "sleeps" automatically when the car is stopped.  It could be an alternative.


# Requirements to run this scripts
python mqtt module : pip3 install paho-mqtt

# Usage / Script Configuration 
You need to tell the script the information it needs to communicate with your mqtt server.
All the needed information should be in the torque_config.py file.  You can rename the file torque_config_sample.py and replace the required information

## Python script Configuration

| Properties   | Description  |
|--------------|--------------|
| LATITUDE_HOME  | Gps coordinate of your home.  Mandatory to calculate distance from home |
| LONGITUDE_HOME | Gps coordinate of your home.  Mandatory to calculate distance from home |
| MY_TIMEZONE    | Timezone of your home to format the timestamp                           |
| MQTT_BROKER    | Addresss of your mqtt broker                                            |
| MQTT_PORT      | Port of your mqtt broker                                                |
| MQTT_TOPIC     | Root of your mqtt topic (For example : mycar/torque)                    |
| MQTT_USER      | MQTT user                                                               |
| MQTT_PASSWORD  | MQTT password                                                           |
| *SEND_TO_MQTT  | List of pid to send to mqtt broker                                      |

*Special Note about the attribute sent to mqtt
There is a special information that will be sent out to mqtt even when you don't select it.
That is the "distance_meter" attribute.  This will be calculated as the distance between the gps coordinate sent by the OBD2 device and the GPS coordinate from the configuration. This attribute will represent the distance in meters from "home" and can be used in home assistant to indicate that the car is home or not.


## Torque configuration
In the torque application, you need to set the following settings : 
![Torque Settings](/images/datalogging_settings.jpg "Torque Settings")

- OBD2 Adapter Settings / Choose Bluetooth Device
- Data Logging & Upload / Log when Torque is started --> True
- Data Logging & Upload / Automatically log GPS --> True
- Data Logging & Upload / Upload to websever --> True
- Data Logging & Upload / Web Logging Intercal --> I fond that every 30 seconds is sufficient
- Data Logging & Upload / WebServer URL --> http://YOUR_IP_OR_ADDRESS_HOSTING_THE_PYTHON_WEBSERVER:PORT/upload
- Data Logging & Upload / Select what to log --> Select the sensors you need
![Torque PID](/images/select_pid.jpg "Torque Select PID")


## Automate starting Torque on your Android phone
I personnaly automated the starting of Torque Application on my android phone with Tasker.
Every time my phone connected to the bluetooth of the OBD2 device, it starts Torque App.


## Home assistant configuration

Config file to add the different mqtt sensors.
You need to add as many as you added in the config file : 
```
mqtt:
  sensor:
    - name: torque_fuel_level
      state_topic: "mycar/torque/fuel_level"
      unique_id: "torque_fuel_level"
      force_update: true
      device_class: battery
      unit: %
    - name: torque_timestamp
      state_topic: "mycar/torque/time"
      unique_id: "torque_mycar_time_updated"
    - name: torque_latitude
      state_topic: "mycar/torque/gps_latitude"
      unique_id: "torque_mycar_gps_latitude"
    - name: torque_longitude
      state_topic: "mycar/torque/gps_longitude"
      unique_id: "torque_mycar_gps_longitude"
    - name: torque_meter_from_home
      state_topic: "mycar/torque/distance_meter"
      unique_id: "torque_mycar_meter_from_home"
      unit: m
```

You can Add this card on your home assistant dashboard
![Home assistant card](/images/hassio.png "Home assistant card")

The icon will change from blue to yellow when the car is not home
And the badge will also change color depending of the fuel level
This is just an example of that is possible with home assistant.

Note that i'm using mushroom themes in home assistant and that it is available from HACS

```
type: custom:mushroom-template-card
primary: 'Sportage.  Essence : {{ states.sensor.torque_fuel_level.state | int }}%'
secondary: 'Dernière mise à jour : {{ states.sensor.torque_timestamp.state }}'
icon: mdi:car
icon_color: |-
  {% if states.sensor.torque_meter_from_home.state | int < 10 %}
            blue
          {% else %}
            red
  {% endif %}
badge_icon: mdi:gas-station
badge_color: |-
  {% if states.sensor.torque_fuel_level.state | int < 20 %}
  red
  {% elif states.sensor.torque_fuel_level.state | int < 40 %}
  yellow
  {% else %}
  blue
  {% endif %}
```



# Docker

This part is a work in progress.  I wanted to create a docker with the python script to host on an unraid or portainer instance, but didn't really test it yet

## Build docker
sudo docker build -t torque_python:1.0 .

## Run docker
sudo docker run --rm -it --name python_torque -p 8014:8011 torque_python:1.0