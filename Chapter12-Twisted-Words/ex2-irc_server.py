from twisted.cred import checkers, portal
from twisted.internet import reactor
from twisted.words import service

wordsRealm = service.InMemoryWordsRealm("example.com")
wordsRealm.createGroupOnRequest = True

checker = checkers.FilePasswordDB("passwords.txt")
portal = portal.Portal(wordsRealm, [checker])

reactor.listenTCP(6667, service.IRCFactory(wordsRealm, portal))
reactor.run()
