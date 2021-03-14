import socket
import logging

logging.getLogger()


class BirdCamera:
    def __init__(self, camera_config):
        self.name = camera_config.get("camera_name")
        self.source = camera_config.get("camera_source")

        if self.source == "network":
            self.port = camera_config.getint("port")
            self.host = camera_config.get("host")
            if self.host is None or self.port is None:
                logging.error("Network camera specified as source,\
                 but networking details incomplete, please update config file.")

        logging.info("Starting Camera: {}, from source: {}".format(self.name, self.source))
