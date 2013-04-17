from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site

from calendar import calendar

class YearPage(Resource):
    def __init__(self, year):
        Resource.__init__(self)
        self.year = year

    def render_GET(self, request):
        return "<html><body><pre>%s</pre></body></html>" % (calendar(self.year),)

class CalendarHome(Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        if name.isdigit():
            return YearPage(int(name))
        else:
            return NoResource()

    def render_GET(self, request):
        return "<html><body>Welcome to the calendar server!</body></html>"

root = CalendarHome()
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
