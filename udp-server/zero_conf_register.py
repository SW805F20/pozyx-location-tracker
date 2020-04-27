import sys
import time
import socket

from zeroconf import ServiceInfo, Zeroconf, IPVersion

class ZeroConfRegister():
    def register_service(self, name):

        ip_version = IPVersion.All

        desc = {'path': 'Untitled Game'}

        info = ServiceInfo(
            "_http._tcp.local.",
            "Lobby {}._http._tcp.local.".format(name),
            addresses=[socket.inet_aton("127.0.0.1")],
            port=80,
            properties=desc,
            server="ash-2.local.",
        )

        zeroconf = Zeroconf(ip_version=ip_version)
        print("Registration of a service, press Ctrl-C to exit...")
        zeroconf.register_service(info)
        try:
            while True:
                time.sleep(0.1)
        finally:
            print("Unregistering...")
            zeroconf.unregister_service(info)
            zeroconf.close()