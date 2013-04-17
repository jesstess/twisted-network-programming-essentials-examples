from zope.interface import implements, Interface

from twisted.cred import checkers, credentials, portal
from twisted.internet import protocol, reactor
from twisted.protocols import basic

class IProtocolAvatar(Interface):
    def logout():
        """
        Clean up per-login resources allocated to this avatar.
        """

class EchoAvatar(object):
    implements(IProtocolAvatar)

    def logout(self):
        pass

class Echo(basic.LineReceiver):
    portal = None
    avatar = None
    logout = None

    def connectionLost(self, reason):
        if self.logout:
            self.logout()
            self.avatar = None
            self.logout = None

    def lineReceived(self, line):
        if not self.avatar:
            username, password = line.strip().split(" ")
            self.tryLogin(username, password)
        else:
            self.sendLine(line)

    def tryLogin(self, username, password):
        self.portal.login(credentials.UsernamePassword(username,
                                                       password),
                          None,
                          IProtocolAvatar).addCallbacks(self._cbLogin,
                                                        self._ebLogin)

    def _cbLogin(self, (interface, avatar, logout)):
        self.avatar = avatar
        self.logout = logout
        self.sendLine("Login successful, please proceed.")

    def _ebLogin(self, failure):
        self.sendLine("Login denied, goodbye.")
        self.transport.loseConnection()

class EchoFactory(protocol.Factory):
    def __init__(self, portal):
        self.portal = portal

    def buildProtocol(self, addr):
        proto = Echo()
        proto.portal = self.portal
        return proto

class Realm(object):
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IProtocolAvatar in interfaces:
            avatar = EchoAvatar()
            return IProtocolAvatar, avatar, avatar.logout
        raise NotImplementedError(
            "This realm only supports the IProtocolAvatar interface.")

realm = Realm()
myPortal = portal.Portal(realm)
checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
checker.addUser("user", "pass")
myPortal.registerChecker(checker)

reactor.listenTCP(8000, EchoFactory(myPortal))
reactor.run()
