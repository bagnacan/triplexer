#
# module for managing (multi-organism and multi-dataset) triplex data
#

import itertools
import logging
import multiprocessing
import sys
from common import *


# logger
logger = logging.getLogger("cache") # TODO: should be set by the calling module

#
# filter the provided data set for allowed duplex-pair comparisons (putative
# triplexes). To spot putative triplexes, each duplex carrying the same target
# has to be compared for seed binding proximity (Saetrom et al. 2007).
# Create a list of comparisons that have to be performed against each scanned
# duplex (for each scanned target)
#
def filter(store, options):
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
            #args=(
            #    core,
            #    namespace,
            #    triplexer_cache,
            #)
        )
        jobs.append(p)
        p.start()
        p.join()

    logger.debug("  ### CACHE ALLOWED DUPLEXES ends ###")
    sys.exit(0)



#
# generate the allowed duplex-pair comparison list
#
#def generate_allowed_comparisons(core, namespace, triplexer_cache):
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

            logger.debug("    Worker %d: Generating allowed triplexes for target %s",
                core, target)

            # compute all possible duplex-pairs

            target_duplexes = store.smembers( str(target + ":duplexes"))

            logger.debug("    Worker %d:   Target found in %d duplexes",
                core, len(target_duplexes))

            duplex_comparisons_all = list(
                itertools.combinations(target_duplexes, 2))

            duplex_comparisons_allowed = []

            logger.debug("    Worker %d:   Comparing each duplex against each other for allowed (binding range) triplexes...",
                core)

            for duplex_comparison in duplex_comparisons_all:

                # get the miRNA-target binding start position
                duplex1 = duplex_comparison[0]
                duplex1_alignment_start = int(
                    store.hget(duplex1, ALIGNMENT_GENE_START))

                logger.debug("    Worker %d:     Duplex %s aligns at %s",
                    core, duplex1, duplex1_alignment_start)

                # get the miRNA-target binding start position
                duplex2 = duplex_comparison[1]
                duplex2_alignment_start = int(
                    store.hget(duplex2, ALIGNMENT_GENE_START))

                logger.debug("    Worker %d:     Duplex %s aligns at %s",
                    core, duplex2, duplex2_alignment_start)

                # compute the binding distance
                binding = abs(
                    duplex1_alignment_start - duplex2_alignment_start)

                logger.debug("    Worker %d:     Duplex binding range is %s",
                    core, binding)

                # putative triplexes have their miRNAs binding a mutual target
                # gene within 13-35 seed distance range (Saetrom et al. 2007).
                # Before proper statistical validation, a candidate triplex
                # conserves this experimentally validated property.

                # test whether the binding distance is within the allowed
                # distance range (Saetrom et al. 2007), and if so, keep the
                # duplex-pair comparison
                if (SEED_MAX_DISTANCE >= binding) and (binding >= SEED_MIN_DISTANCE):

                    logger.debug("    Worker %d:       Duplex %s vs. %s --> range allowed (%d >= %d >= %d). Triplex kept",
                        core, duplex1, duplex2, SEED_MAX_DISTANCE, binding, SEED_MIN_DISTANCE)

                    duplex_comparisons_allowed.append(duplex_comparison)

                else:
                    logger.debug("    Worker %d:       Duplex %s vs. %s --> range disallowed. Triplex ignored",
                        core, duplex1, duplex2)

            # cache all allowed duplex-pair comparisons
            if duplex_comparisons_allowed:
                statistics_targets_binding  += 1
                statistics_duplexes_binding += len(duplex_comparisons_allowed)

                # cache the popped target in a set of allowed seed
                # binding range targets
                store.sadd(str(namespace + ":targets:binding"),
                    target)

                logger.debug("    Worker %d:   Cached target in allowed seed binding range targets",
                    core)

                # cache the allowed duplex comparisons
                store.sadd(str(target + ":duplexes:binding"),
                    duplex_comparisons_allowed)

                logger.debug("    Worker %d:   Target %s forms %d allowed binding range triplexes among the %d possible duplex comparisons",
                    core, target, len(duplex_comparisons_allowed),
                    len(duplex_comparisons_all))

        else:
            break

    logger.info("    Worker %d: Examined %d targets, %d of which are targeted by %d putative triplexes",
        core, statistics_targets_all, statistics_targets_binding,
        statistics_duplexes_binding)

