import socket
import logging

logging.getLogger()


class Sensor:
    def __init__(self, sensor_config):
        self.type = sensor_config.get("sensor_app")
        self.port = sensor_config.getint("port", 5555)
        self.host = sensor_config.get("host", "")
        logging.debug("Starting sensor type: {}".format(self.type))

    def get_sensor_data(self):
        logging.debug("Starting sensor reading on UDP host:port : {}:{}".format(self.host, self.port))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        s.bind((self.host, self.port))

        message, address = s.recvfrom(8192)
        logging.debug("Recieved Sensor data\nMessage: {}\nAddress: {}".format(message, address))

        # for Sensorstream:
        # timestamp (   b'132253.62497,
        # Accel         3,   0.190,  9.663,  1.840,
        # Gyro          4,  -0.000,  0.000, -0.000,
        # Mag field     5, -88.133,-227.426, 63.067,
        # GPS would be here but in the source for Sensorstream GPS is commented out for some reason
        #  Ref: https://sourceforge.net/projects/smartphone-imu/ in the PreferencesActivity.java file
        # Orientation   81, 122.569,-79.197,  1.127,
        # Linear Acc.   82,   0.003, -0.033,  0.001,
        # Gravity       83,   0.193,  9.634,  1.838,
        # Rotation Vect.84,   0.300, -0.563, -0.673,
        # Pressure      85, 1011.466,
        # Batt Temp     86, 24')
        #

        if len(message) < 220:
            # if there is not enough data die
            # 220 b/c rigorous testing... namely I checked the return len of the string once
            return None

        # TODO regex split this crap

        return message, address
