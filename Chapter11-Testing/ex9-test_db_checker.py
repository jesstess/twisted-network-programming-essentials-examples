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

    def test_requestAvatarIdBadCredentials(self):
        """
        Calling requestAvatarId with invalid credentials raises an
        UnauthorizedLogin error.
        """
        def fakeRunqueryBadPassword(query, username):
            d = Deferred()
            reactor.callLater(1, d.callback, (("user", "badpass"),))
            return d

        creds = credentials.UsernameHashedPassword("user", "pass")
        checker = DBCredentialsChecker(fakeRunqueryBadPassword, "fake query")
        d = checker.requestAvatarId(creds)

        def checkError(result):
            self.assertEqual(result.message, "Password mismatch")
        return self.assertFailure(d, UnauthorizedLogin).addCallback(checkError)

    def test_requestAvatarIdNoUser(self):
        """
        Calling requestAvatarId with credentials for an unknown user
        raises an UnauthorizedLogin error.
        """
        def fakeRunqueryMissingUser(query, username):
            d = Deferred()
            reactor.callLater(0, d.callback, ())
            return d

        creds = credentials.UsernameHashedPassword("user", "pass")
        checker = DBCredentialsChecker(fakeRunqueryMissingUser, "fake query")
        d = checker.requestAvatarId(creds)

        def checkError(result):
            self.assertEqual(result.message, "User not in database")
        return self.assertFailure(d, UnauthorizedLogin).addCallback(checkError)
