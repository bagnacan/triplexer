#
# module for managing microrna.org data
#


import logging
import os
import redis
import sys
from common import *


SEPARATOR = ":"


# microrna.org target predictions are organised in a file storing one duplex
# per line. Each duplex is described in terms of the following fields
MIRNA_ACCESSION = "mirbase_acc"
MIRNA_NAME      = "mirna_name"
TARGET_GENE_ID     = "gene_id"
TARGET_GENE_SYMBOL = "gene_symbol"
TRANSCRIPT_ID     = "transcript_id"
TRANSCRIPT_ID_EXT = "ext_transcript_id"
ALIGNMENT             = "alignment"
ALIGNMENT_MIRNA       = "mirna_alignment"
ALIGNMENT_GENE        = "gene_alignment"
ALIGNMENT_MIRNA_START = "mirna_start"
ALIGNMENT_MIRNA_END   = "mirna_end"
ALIGNMENT_GENE_START  = "gene_start"
ALIGNMENT_GENE_END    = "gene_end"
ALIGNMENT_SCORE       = "align_score"
GENOME_COORDINATES    = "genome_coordinates"
CONSERVATION = "conservation"
SEED_TYPE    = "seed_cat"
ENERGY       = "energy"
MIRSRV_SCORE = "mirsvr_score"
CHAR_FIELD_SEPARATOR = "\t"
CHAR_HEADING = "#"


# microrna.org duplex field organisation
duplex = {
    MIRNA_ACCESSION:        0,
    MIRNA_NAME:             1,
    TARGET_GENE_ID:         2,
    TARGET_GENE_SYMBOL:     3,
    TRANSCRIPT_ID:          4,
    TRANSCRIPT_ID_EXT:      5,
    ALIGNMENT_MIRNA:        6,
    ALIGNMENT:              7,
    ALIGNMENT_GENE:         8,
    ALIGNMENT_MIRNA_START:  9,
    ALIGNMENT_MIRNA_END:   10,
    ALIGNMENT_GENE_START:  11,
    ALIGNMENT_GENE_END:    12,
    GENOME_COORDINATES:    13,
    CONSERVATION:          14,
    ALIGNMENT_SCORE:       15,
    SEED_TYPE:             16,
    ENERGY:                17,
    MIRSRV_SCORE:          18
}


# logger
logger = logging.getLogger("microrna.org")



#
# cache the putative triplexes
#
def cache(store, options):
    """
    Caches the putative gene targets and miRNA pairs that comply to the
    formation constraints of an RNA triplex.
    """

    logger.info("Finding putative triplexes from microrna.org data")

    # caching namespace
    namespace = str(
        options[OPT_NAMESPACE] + SEPARATOR +
        options[OPT_ORGANISM] + SEPARATOR +
        options[OPT_GENOME])

    # retrieve all duplexes, organising them by target gene
    cache_duplexes(store, options[OPT_FILE], namespace)



#
# read the microrna.org target prediction file
#
def cache_duplexes(store, in_file, namespace):
    """
    Reads the supplied microrna.org target prediction file, and retrieves a
    list of all stored duplexes.
    """

    count_lines    = 0
    count_duplexes = 0

    logger.debug("  ### CACHE DUPLEXES starts ###")

    logger.info("  Reading duplexes from %s ...", in_file)

    # each line represents a duplex, holding a target id, a miRNA id, and all
    # attributes related to the complex.
    # Multiple lines can refer to the same target.
    # Store each duplex in a target-specific redis set.

    with open(in_file, 'r') as in_file:

        # setup a redis set to contain all duplex's targets
        targets = str(namespace + ":targets")

        for line in in_file:

            count_lines += 1

            if not line.startswith(CHAR_HEADING):

                count_duplexes += 1

                # create a redis hash to hold all attributes of the current
                # duplex line.
                # Each redis hash represents a duplex.
                # Multiple duplexes can be relative to a same target.
                logger.debug("    Reading duplex on line %d",
                    count_lines)

                target_hash = get_hash(line)
                duplex = str(namespace +
                    ":duplex:line" + str(count_lines))
                target = str(namespace +
                    ":target:" + target_hash[TRANSCRIPT_ID])
                target_duplexes = str(namespace +
                    ":target" + target_hash[TRANSCRIPT_ID] + ":duplexes")

                # cache
                try:
                    # cache the dictionary representation of the current duplex
                    # in a redis hash
                    store.hmset(duplex, target_hash)
                    logger.debug(
                        "      Cached key-value pair duplex %s with attributes from line %d",
                        duplex, count_lines
                    )

                    # cache the redis hash reference in a redis set of duplexes
                    # sharing the same target
                    store.sadd(target_duplexes, duplex)
                    logger.debug(
                        "      Cached duplex id %s as relative to target %s",
                        duplex, target
                    )

                    # cache the target in a redis set
                    store.sadd(targets, target)
                    logger.debug("      Cached target id %s", target)

                except redis.ConnectionError:
                    logger.error("    Redis cache not running. Exiting")
                    sys.exit(1)


                # in a late processing step, "workers" will take each target,
                # and compare each hash with each others to spot for miRNA
                # binding in close proximity.
                # The comparison problem will be quadratic.

    in_file.close()

    logger.info(
        "    Found %s RNA duplexes across %s target genes",
        str(count_duplexes), str(store.scard(targets))
    )

    logger.debug("  ### CACHE DUPLEXES ends ###")



#
# return a redis hash representation of the current line
#
def get_hash(line):
    """
    Returns a redis hash representation of the given input line.
    """

    # split the line
    entry = line.rstrip().lstrip().split(CHAR_FIELD_SEPARATOR)

    # build a dictionary representation from all fields in the line
    result = {
        MIRNA_ACCESSION: entry[ duplex[MIRNA_ACCESSION] ],
        MIRNA_NAME:      entry[ duplex[MIRNA_NAME] ],
        TARGET_GENE_ID:     entry[ duplex[TARGET_GENE_ID] ],
        TARGET_GENE_SYMBOL: entry[ duplex[TARGET_GENE_SYMBOL] ],
        TRANSCRIPT_ID:     entry[ duplex[TRANSCRIPT_ID] ],
        TRANSCRIPT_ID_EXT: entry[ duplex[TRANSCRIPT_ID_EXT] ],
        ALIGNMENT:             entry[ duplex[ALIGNMENT] ],
        ALIGNMENT_MIRNA:       entry[ duplex[ALIGNMENT_MIRNA] ],
        ALIGNMENT_GENE:        entry[ duplex[ALIGNMENT_GENE] ],
        ALIGNMENT_MIRNA_START: entry[ duplex[ALIGNMENT_MIRNA_START] ],
        ALIGNMENT_MIRNA_END:   entry[ duplex[ALIGNMENT_MIRNA_END] ],
        ALIGNMENT_GENE_START:  entry[ duplex[ALIGNMENT_GENE_START] ],
        ALIGNMENT_GENE_END:    entry[ duplex[ALIGNMENT_GENE_END] ],
        ALIGNMENT_SCORE:       entry[ duplex[ALIGNMENT_SCORE] ],
        GENOME_COORDINATES: entry[ duplex[GENOME_COORDINATES] ],
        CONSERVATION: entry[ duplex[CONSERVATION] ],
        SEED_TYPE:    entry[ duplex[SEED_TYPE] ],
        ENERGY:       entry[ duplex[ENERGY] ],
        MIRSRV_SCORE: entry[ duplex[MIRSRV_SCORE] ]
    }

    return result
