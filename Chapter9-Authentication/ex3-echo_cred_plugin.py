from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.cred import credentials, portal, strcred
from twisted.plugin import IPlugin
from twisted.python import usage

from zope.interface import implements

from echo_cred import EchoFactory, Realm

class Options(usage.Options, strcred.AuthOptionMixin):
    supportedInterfaces = (credentials.IUsernamePassword,)
    optParameters = [["port", "p", 8000,
                      "The port number to listen on."]]

class EchoServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "echo"
    description = "A TCP-based echo server."
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from EchoFactory.
        """
        p = portal.Portal(Realm(), options["credCheckers"])
        return internet.TCPServer(int(options["port"]),
	                          EchoFactory(p))

serviceMaker = EchoServiceMaker()
