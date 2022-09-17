
class TorqueSensor:
    
    def __init__(self, name: str, field: str, unit: str):
        self.name = name
        self.field = field
        self.unit = unit


TORQUE_DICTIONARY = {
            #distance_meter is a special case that is not an attribute of obd2, but is calculated when GPS values are there        
            "eml": TorqueSensor("Account", "account",  ""),
            "v": TorqueSensor("Version", "version", ""),
            "session": TorqueSensor("Session", "session", ""),
            "time": TorqueSensor("TimeStamp", "time", ""),
            "k5": TorqueSensor("Engine Coolant Temperature", "engine_coolant_temp","C"),
            "k4": TorqueSensor("Engine Load", "engine_load", "%"),
            "k43": TorqueSensor("Engine Load (Absolute)", "engine_load_absolute", "%"),
            "kc": TorqueSensor("Engine RPM", "engine_rpm", "rpm"),
            "k2f": TorqueSensor("Fuel Level", "fuel_level", "%"),
            "kff1010": TorqueSensor("GPS Altitude", "gps_altitude", "m"),
            "kff1006": TorqueSensor("GPS Latitude", "gps_latitude", ""),
            "kff1005": TorqueSensor("GPS Longitude", "gps_longitude", ""),
            "kff1226": TorqueSensor("Horsepower (At the wheels)", "horsepower_at_wheel", "hp"),
            "kf": TorqueSensor("Intake Air Temperature", "intake_air_temperature", "C"),
            "kff1207": TorqueSensor("Litres Per 100 km (instant)", "litres_per_100_instant", "l/100km"),
            "kff1296": TorqueSensor("Percentage of City Driving", "driving_city", "%"),
            "kff1297": TorqueSensor("Percentage of Highway Driving", "driving_highway", "%"),
            "kff1298": TorqueSensor("Percentage of Idle Driving", "driving_idle", "%"),
            "kff1001": TorqueSensor("Speed (GPS)", "speed_gps", "km/h"),
            "kd": TorqueSensor("Speed (OBD)", "speed_obd", "km/h"),
            "kff1007": TorqueSensor("GPS Bearing", "gps_bearing", ""),
            "k49": TorqueSensor("Accelerator Pedal position", "accelerator_pedal_position", "%"),
            "kff1238": TorqueSensor("Voltage (ODB Adapter)", "voltage_odb_adapter", "V"),
            "id": TorqueSensor("ID", "id", ""),
      
    }

