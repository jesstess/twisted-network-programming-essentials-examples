from twisted.python import log
from twisted.python import logfile

# Log to /tmp/test.log ... test.log.N, rotating every 100 bytes.
f = logfile.LogFile("test.log", "/tmp", rotateLength=100)
log.startLogging(f)

log.msg("First message")

# rotate manually
f.rotate()

for i in range(5):
    log.msg("Test message", i)

log.msg("Last message")
