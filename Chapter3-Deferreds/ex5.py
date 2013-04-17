from twisted.internet.defer import Deferred

def callback1(result):
    print "Callback 1 said:", result
    return result

def callback2(result):
    print "Callback 2 said:", result

def callback3(result):
    raise Exception("Callback 3")

def errback1(failure):
    print "Errback 1 had an an error on", failure
    return failure

def errback2(failure):
    raise Exception("Errback 2")

def errback3(failure):
    print "Errback 3 took care of", failure
    return "Everything is fine now."
