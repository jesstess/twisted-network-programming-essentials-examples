from twisted.internet import reactor
from twisted.web import server, resource
from twisted.cred import portal, checkers
from twisted.conch import manhole, manhole_ssh
class LinksPage(resource.Resource):
    isLeaf = 1
    def __init__(self, links):
        resource.Resource.__init__(self)
        self.links = links
    def render(self, request):
        return "<ul>" + "".join([
            "<li><a href='%s'>%s</a></li>" % (link, title)
            for title, link in self.links.items()]) + "</ul>"
links = {'Twisted': 'http://twistedmatrix.com/',
         'Python': 'http://python.org'}
site = server.Site(LinksPage(links))
reactor.listenTCP(8000, site)
def getManholeFactory(namespace, **passwords):
    realm = manhole_ssh.TerminalRealm()
    def getManhole(_): return manhole.Manhole(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    p.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    f = manhole_ssh.ConchFactory(p)
    return f
reactor.listenTCP(2222, getManholeFactory(globals(), admin='aaa'))
reactor.run()
