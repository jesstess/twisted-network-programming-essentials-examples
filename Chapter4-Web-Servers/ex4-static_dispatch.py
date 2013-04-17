from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

root = File('/var/www/mysite')
root.putChild("doc", File("/usr/share/doc"))
root.putChild("logs", File("/var/log/mysitelogs"))
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
