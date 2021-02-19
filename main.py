import configparser
from datetime import datetime
import logging
import socket
import sys
from time import sleep

import Sensors

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
edge_config_file = 'birdcam_edge.ini'
edge_config = dict()


def get_configuration():
    # reads configuration INI file and returns dict of variables
    config = configparser.ConfigParser()
    try:
        config.read(edge_config_file)
        logging.debug("Read Config file: {}".format(edge_config_file))
        return config
    except Exception as e:
        logging.error("Could not read config file, exception raised: {}".format(e))
        sys.exit(1)


def is_valid_hours():
    # uses start/end times to know when to continue collecting data.
    curr = datetime.now()
    if edge_config['DEFAULT'].getint("start_time") <= curr.hour < edge_config['DEFAULT'].getint("end_time"):
        logging.info("{} is inside valid hours".format(curr.hour))
        return True
    logging.info("{} is outside valid hours".format(curr.hour))
    return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    edge_config = get_configuration()

    while is_valid_hours():
        logging.debug("In valid hours, continuing")

        sensor = Sensors.Sensor(edge_config["Sensor_Definition"])
        print(sensor.get_sensor_data())
        # collect Sensor data
        # get image
        # update image datals
        # upload pic to S3
        # write data to DDB

        # sleep for a timeout
        sleep(edge_config['DEFAULT'].getint("sleep_delay"))

