#!/usr/bin/sudo python
from jumpscale import j
import gipc
zdb_start=True
monitor = True
rack=j.servers.gworld.server_rack_get(monitor=monitor, gedis_instance_name='test')

if zdb_start:
    cl = j.clients.zdb.testdb_server_start_client_get(start=True)  #starts & resets a zdb in seq mode with name test

ws_dir = j.clients.git.getContentPathFromURLorPath("https://github.com/threefoldtech/digital_me/tree/development/digitalme")

server = j.servers.gedis.configure(host = "localhost", port = "8000", ssl = False, \
    zdb_instance = "test",secret = "", app_dir = ws_dir, instance='test')

redis_server = j.servers.gedis.geventservers_get("test")
rack.add("gedis",redis_server)

#configure a local webserver server (the master one)
j.servers.web.configure(instance="test", port=5050,port_ssl=0, host="localhost", secret="", ws_dir=ws_dir)

#use jumpscale way of doing wsgi server (make sure it exists already)
ws=j.servers.web.geventserver_get("test")
rack.add("web",ws)

# dnsserver=j.servers.dns.get(5355)
# rack.add(dnsserver)

rack.start()

gevent.sleep(1000000000)

rack.stop()
