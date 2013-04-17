from twisted.trial import unittest
from twisted.cred import credentials
from twisted.cred.error import UnauthorizedLogin
from twisted.internet import reactor
from twisted.internet.defer import Deferred

from db_checker import DBCredentialsChecker

class DBCredentialsCheckerTestCase(unittest.TestCase):

    def test_requestAvatarIdGoodCredentials(self):
        """
        Calling requestAvatarId with correct credentials returns the
        username.
        """
	def fakeRunqueryMatchingPassword(query, username):
            d = Deferred()
            reactor.callLater(0, d.callback, (("user", "pass"),))
            return d

        creds = credentials.UsernameHashedPassword("user", "pass")
        checker = DBCredentialsChecker(fakeRunqueryMatchingPassword,
                                       "fake query")
        d = checker.requestAvatarId(creds)

        def checkRequestAvatarCb(result):
	    self.assertEqual(result, "user")
        d.addCallback(checkRequestAvatarCb)
	return d
