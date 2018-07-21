import logging
import redis
from common import *


# logger
logger = logging.getLogger("microrna.org")



def cache(options):
    """
    Caches the putative gene targets and miRNA pairs that comply to the
    formation constraints of an RNA triplex.
    """

    # redis cache
    logger.info("Setting up storage at %s", options[OPT_LOCATION])
    cache = redis.StrictRedis(
        host=options[OPT_LOCATION].split(":")[0],
        port=options[OPT_LOCATION].split(":")[1],
        db=options[OPT_LOCATION_DB])

    logger.info("Finding putative triplexes from microrna.org data")

    # caching namespace
    namespace = str(options[OPT_NAMESPACE] + ":" +  options[OPT_ORGANISM] + ":" + options[OPT_GENOME])

    # retrieve all duplexes, organising them by target gene
    #cache_duplexes(options[OPT_FILE], namespace, options[OPT_STORAGE])
