from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

class TestPage(Resource):
    isLeaf = True
    def render_POST(self, request):
        return request.content.read()[::-1]

resource = TestPage()
factory = Site(resource)
reactor.listenTCP(8000, factory)
reactor.run()
