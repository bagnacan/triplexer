#
# module for managing microrna.org data
#


import itertools
import logging
import multiprocessing
import os
import redis
import sys
from common import *



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
        options[OPT_GENOME]
    )

    # retrieve all duplexes, organising them by target gene
    cache_duplexes(store, options[OPT_FILE], namespace)



#
# read the microrna.org target prediction file
#
def cache_duplexes(store, in_file, namespace):
    """
    Reads the supplied microrna.org target prediction file, and caches all
    stored duplexes within it.
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

                duplex = str(
                    namespace +
                    ":duplex:line" +
                    str(count_lines)
                )

                target = str(
                    namespace +
                    ":target:" +
                    target_hash[TRANSCRIPT_ID]
                )

                target_duplexes = str(
                    namespace +
                    ":target" +
                    target_hash[TRANSCRIPT_ID] +
                    ":duplexes"
                )

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



#
# filter the provided data set for allowed duplex-pair comparisons (putative
# triplexes). To spot putative triplexes, each duplex carrying the same target
# has to be compared for seed binding proximity (Saetrom et al. 2007).
# Create a list of comparisons that have to be performed against each scanned
# duplex (for each scanned target)
# TODO: move out onceother input modules are implemented
def allowed(store, options):
    """
    Retrieves each target and set of associated duplexes, and builds a list
    containing all possible comparisons among those duplexes whose seed-binding
    distance resides within the allowed nt. range (Saetrom et al. 2007).
    This process is carried out on multiple targets in parallel.
    """

    logger.debug("  ### CACHE ALLOWED DUPLEXES starts ###")

    logger.info("  Finding allowed duplex-pair comparisons among each target's duplex ...")


    # generate all comparison jobs in parallel, assigning the same job to as
    # many processes as number of given cores
    jobs = []
    for core in range(int(options[OPT_CORES])):
        p = multiprocessing.Process(
            target=generate_allowed_comparisons,
            args=(store, options, core)
        )
        jobs.append(p)
        p.start()
        p.join()

    logger.debug("  ### CACHE ALLOWED DUPLEXES ends ###")
    sys.exit(0)



#
# generate the allowed duplex-pair comparison list
# TODO: move out onceother input modules are implemented
def generate_allowed_comparisons(store, options, core):
    """
    Takes each target gene's cached duplex, and compares them all to spot
    duplexes whose miRNA binds the mutual target within the seed binding range
    outlined by Saetrom et al. (2007). This range defines a constraint for the
    formation of a putative RNA triplex. Duplex pairs that conserve this
    constraint are then cached for later statistical validation.
    """

    namespace = options[OPT_NAMESPACE]

    # per-worker summary statistics
    statistics_targets_all      = 0
    statistics_targets_binding  = 0
    statistics_duplexes_binding = 0

    # work until there are available targets :)
    while True:

        # get the next available target, and create all allowed duplex-pair
        # comparisons from its associated duplex set. Regardless of the miRNA
        # IDs (the same miRNA can in fact bind the same target at different
        # positions), test whether the binding distance is within the binding
        # range outlined by Saetrom et al. (Saetrom et al. 2007)

        target = store.spop( str(namespace + ":targets") )

        # (popped targets will be cached in another set to allow further
        # operations, or ignored in case they do not form any allowed RNA
        # triplex)

        if target:
            statistics_targets_all += 1

            logger.debug(
                "    Worker %d: Generating allowed triplexes for target %s",
                core, target)

            # compute all possible duplex-pairs

            target_duplexes = store.smembers( str(target + ":duplexes"))

            logger.debug(
                "    Worker %d:   Target found in %d duplexes",
                core, len(target_duplexes)
            )

            duplex_comparisons_all = list(
                itertools.combinations(target_duplexes, 2)
            )

            duplex_comparisons_allowed = []

            logger.debug(
                "    Worker %d:   Comparing each duplex against each other for allowed (binding range) triplexes...",
                core
            )

            for duplex_comparison in duplex_comparisons_all:

                # get the miRNA-target binding start position
                duplex1 = duplex_comparison[0]
                duplex1_alignment_start = int(
                    store.hget(duplex1, ALIGNMENT_GENE_START)
                )

                logger.debug(
                    "    Worker %d:     Duplex %s aligns at %s",
                    core, duplex1, duplex1_alignment_start
                )

                # get the miRNA-target binding start position
                duplex2 = duplex_comparison[1]
                duplex2_alignment_start = int(
                    store.hget(duplex2, ALIGNMENT_GENE_START)
                )

                logger.debug(
                    "    Worker %d:     Duplex %s aligns at %s",
                    core, duplex2, duplex2_alignment_start
                )

                # compute the binding distance
                binding = abs(
                    duplex1_alignment_start - duplex2_alignment_start
                )

                logger.debug(
                    "    Worker %d:     Duplex binding range is %s",
                    core, binding
                )

                # putative triplexes have their miRNAs binding a mutual target
                # gene within 13-35 seed distance range (Saetrom et al. 2007).
                # Before proper statistical validation, a candidate triplex
                # conserves this experimentally validated property.

                # test whether the binding distance is within the allowed
                # distance range (Saetrom et al. 2007), and if so, keep the
                # duplex-pair comparison
                if (SEED_MAX_DISTANCE >= binding) and (binding >= SEED_MIN_DISTANCE):

                    logger.debug(
                        "    Worker %d:       Duplex %s vs. %s --> range allowed (%d >= %d >= %d). Triplex kept",
                        core, duplex1, duplex2, SEED_MAX_DISTANCE, binding, SEED_MIN_DISTANCE
                    )

                    duplex_comparisons_allowed.append(duplex_comparison)

                else:
                    logger.debug(
                        "    Worker %d:       Duplex %s vs. %s --> range disallowed. Triplex ignored",
                        core, duplex1, duplex2
                    )

            # cache all allowed duplex-pair comparisons
            if duplex_comparisons_allowed:
                statistics_targets_binding  += 1
                statistics_duplexes_binding += len(duplex_comparisons_allowed)

                # cache the popped target in a set of allowed seed
                # binding range targets
                store.sadd(str(namespace + ":targets:binding"), target)

                logger.debug(
                    "    Worker %d:   Cached target in allowed seed binding range targets",
                    core
                )

                # cache the allowed duplex comparisons
                store.sadd(
                    str(target + ":duplexes:binding"),
                    duplex_comparisons_allowed
                )

                logger.debug(
                    "    Worker %d:   Target %s forms %d allowed binding range triplexes among the %d possible duplex comparisons",
                    core, target, len(duplex_comparisons_allowed),
                    len(duplex_comparisons_all)
                )

        else:
            break

    logger.info(
        "    Worker %d: Examined %d targets, %d of which are targeted by %d putative triplexes",
        core, statistics_targets_all, statistics_targets_binding,
        statistics_duplexes_binding
    )

