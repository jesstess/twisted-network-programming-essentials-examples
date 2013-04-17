from twisted.test import proto_helpers
from twisted.trial import unittest

from chatserver import ChatFactory

class ChatServerTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = ChatFactory()
        self.proto = self.factory.buildProtocol(("localhost", 0))
        self.transport = proto_helpers.StringTransport()
        self.proto.makeConnection(self.transport)

    def test_connect(self):
        self.assertEqual(self.transport.value(),
                         "What's your name?\r\n")

    def test_register(self):
        self.assertEqual(self.proto.state, "REGISTER")
        self.proto.lineReceived("jesstess")
        self.assertIn("jesstess", self.proto.factory.users)
        self.assertEqual(self.proto.state, "CHAT")

    def test_second_user(self):
        self.proto.lineReceived("jesstess")

        proto2 = self.factory.buildProtocol(("localhost", 0))
        transport2 = proto_helpers.StringTransport()
        proto2.makeConnection(transport2)

        self.transport.clear()
        proto2.lineReceived("adamf")

        self.assertEqual(self.transport.value(),
                         "adamf has joined the channel.\r\n")
