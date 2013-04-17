from twisted.test import proto_helpers
from twisted.trial import unittest

from echo import EchoFactory

class EchoServerTestCase(unittest.TestCase):
    def test_echo(self):
        factory = EchoFactory()
        self.proto = factory.buildProtocol(("localhost", 0))
        self.transport = proto_helpers.StringTransport()

        self.proto.makeConnection(self.transport)
        self.proto.dataReceived("test\r\n")
        self.assertEqual(self.transport.value(), "test\r\n")
