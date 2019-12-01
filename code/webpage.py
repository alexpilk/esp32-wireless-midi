from code.lib.microWebSrv import MicroWebSrv
from code.api import route_handlers


def run():
    server = MicroWebSrv(routeHandlers=route_handlers)
    server.Start(threaded=True)
