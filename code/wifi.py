import network
from code import config


def connect_station(configuration: config.StationConfig):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(configuration.SSID, configuration.PASSWORD)
    station.ifconfig((configuration.IP, configuration.SUBNET_MASK, configuration.GATEWAY, '8.8.8.8'))


def connect_access_point(configuration: config.AccessPointConfig):
    raise NotImplementedError


def start_wifi():
    if config.ACCESS_POINT_MODE:
        connect_access_point(config.AccessPointConfig())
    else:
        connect_station(config.StationConfig())
