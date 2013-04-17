import sys
from twisted.python import log

log.startLogging(sys.stdout)
log.msg("Starting experiment")

log.msg("Logging an exception")

try:
    1 / 0
except ZeroDivisionError, e:
    log.err(e)

log.msg("Ending experiment")
