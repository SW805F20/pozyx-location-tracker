import sys
import time
import select
import socket
import bonjour



# Callback for service registration
def register_callback(sd_ref, flags, error_code, name, regtype, domain, context):
    print("Service registered:", name, regtype, domain)


if len(sys.argv) < 4:
    print("Usage: register.py servicename regtype port")
    sys.exit(1)

servicename = sys.argv[1]
regtype = sys.argv[2]
port = int(sys.argv[3])
# Allocate a service discovery reference and register the specified service
flags = 0
interface_index = 0
domain = ''
host = ''
txt_len = 0
txt_record = ''
user_data = None
serviceRef = bonjour.AllocateDNSServiceRef()
ret = bonjour.pyDNSServiceRegister(serviceRef,
                                   flags,
                                   interface_index,
                                   servicename,
                                   regtype,
                                   domain,
                                   host,
                                   port,
                                   txt_len,
                                   txt_record,
                                   register_callback,
                                   user_data)


if ret != bonjour.kDNSServiceErr_NoError:
    print("error %d returned; exiting" % ret)
    sys.exit(ret)

# Get the socket and loop
fd = bonjour.DNSServiceRefSockFD(serviceRef)
while 1:
    ret = select.select([fd], [], [])
    ret = bonjour.DNSServiceProcessResult(serviceRef)

# Deallocate the service discovery ref
bonjour.DNSServiceRefDeallocate(serviceRef)

