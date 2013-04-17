# Errata note: when TNPE 2ed was first printed, Twisted 12.0.0 was the latest
# version of Twisted. In Example 3-2 from that print version, a bare string is
# passed to the errback method, i.e.
#
#    d.errback("Triggering errback.")
#
# Passing bare strings to the errback method was deprecated in Twisted 12.3.0. A
# Failure or Exception must now be passed instead.

from twisted.internet.defer import Deferred

def myErrback(failure):
    print failure

d = Deferred()
d.addErrback(myErrback)
d.errback(ValueError("Triggering errback."))
