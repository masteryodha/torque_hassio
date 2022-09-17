FROM python:3
ADD torque_load.py /
ADD torque_config.py /
ADD torque_sensor.py /

EXPOSE 8080

RUN pip install --no-cache-dir paho-mqtt

CMD [ "python3", "./torque_load.py" ]
