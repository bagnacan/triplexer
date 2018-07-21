import logging


MODULE = "microrna.org"



# logger
logger = logging.getLogger(MODULE)



def cache(options):
    """
    Caches the putative gene targets and miRNA pairs that comply to the
    formation constraints of an RNA triplex.
    """
    global OPT_STORAGE
    global OPT_ORGANISM
    global OPT_GENOME
    global OPT_FILE

    logger.info("Finding putative triplexes from microrna.org data")

    # caching namespace
    namespace = ":".join(MODULE, options[OPT_ORGANISM], options[OPT_VERSION])

    # retrieve all duplexes, organising them by target gene
    cache_duplexes(options[OPT_FILE], namespace, options[OPT_STORAGE])

    
