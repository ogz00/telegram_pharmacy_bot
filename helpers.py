import codecs
import glob
import logging.handlers as handlers
import os
import time
import zipfile


class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """

    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes
        self.suffix = "%Y-%m-%d_%H-%M-%S"

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            # due to non-posix-compliant Windows feature
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0

    """
       Extended version of TimedRotatingFileHandler that compress logs on rollover.
       """

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """

        self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        # t = self.rolloverAt - self.interval
        t = int(time.time())
        timeTuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            # find the oldest log file and delete it
            s = glob.glob(self.baseFilename + ".20*")
            if len(s) > self.backupCount:
                s.sort()
                os.remove(s[0])
        # print "%s -> %s" % (self.baseFilename, dfn)
        if self.encoding:
            self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
        else:
            self.stream = open(self.baseFilename, 'w')

        t = int(time.time())
        if t >= self.rolloverAt:
            self.rolloverAt = self.rolloverAt + self.interval

        if os.path.exists(dfn + ".zip"):
            os.remove(dfn + ".zip")
        file = zipfile.ZipFile(dfn + ".zip", "w")
        file.write(dfn, os.path.basename(dfn), zipfile.ZIP_DEFLATED)
        file.close()
        os.remove(dfn)