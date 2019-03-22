import sync
import time
import logging
import config

logging.basicConfig(format='%(levelname)s\t%(message)s', level=logging.DEBUG)

 #contains databse accessing methods

POLLING_DELAY = 10

while True:
    """
    Run a loop checking and updating the database indexing state with sync
    """
    time.sleep(POLLING_DELAY)
    try:
        sync.synchronize(config.importer_links, config.data_accessor)
    except Exception as e:
        logging.error('Attempted to synchronize')
        logging.error(str(e))
