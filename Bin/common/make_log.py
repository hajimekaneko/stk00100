import logging
import logging.handlers

import stk00100_iniget as Ini
from stk00100_iniget import vgfGetIni



# loggerを初期化する関数
def setup_logger(name):
    vgfGetIni()
    logfile = Ini.vgs_LogFile
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even DEBUG messages
    fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=100000, backupCount=10)
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)-20s - %(funcName)-15s - %(message)s', '%Y-%m-%d %H:%M:%S')
    fh.setFormatter(fh_formatter)

    # create console handler with a INFO log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

if __name__ == '__main__':
    from stk00100_iniget import vgfGetIni
    vgfGetIni()
    logger = setup_logger(__name__)
    logger.info("ree")
    logger.warning("ree")
    logger.debug("ree")
    logger.warning("ree")
