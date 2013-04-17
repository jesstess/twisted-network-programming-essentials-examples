from twisted.test import proto_helpers
from twisted.trial import unittest
from twisted.internet import reactor, task

from pp import EchoProcessProtocol

class EchoProcessProtocolTestCase(unittest.TestCase):
    def test_terminate(self):
        """
        EchoProcessProtocol terminates itself after 10 seconds.
        """
        self.terminated = False

        def fakeTerminateProcess():
            self.terminated = True

        clock = task.Clock()
        pp = EchoProcessProtocol(clock)
        pp.terminateProcess = fakeTerminateProcess
        transport = proto_helpers.StringTransport()
        pp.makeConnection(transport)

        self.assertFalse(self.terminated)
        clock.advance(10)
        self.assertTrue(self.terminated)
