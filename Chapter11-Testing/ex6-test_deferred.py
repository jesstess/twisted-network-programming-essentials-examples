from twisted.internet.defer import Deferred
from twisted.internet import reactor
from twisted.trial import unittest

class DeferredTestCase(unittest.TestCase):
    def slowFunction(self):
        d = Deferred()
        reactor.callLater(1, d.callback, ("foo"))
        return d

    def test_slowFunction(self):
        def cb(result):
            self.assertEqual(result, "foo")

        d = self.slowFunction()
        d.addCallback(cb)
