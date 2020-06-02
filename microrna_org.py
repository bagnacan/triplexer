#
# module for managing microrna.org data
#


import itertools
import logging
import pymysql
import re
import redis
import requests
import sys
from bs4 import BeautifulSoup
from common import *
from multiprocessing import Process
from pathlib import Path
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC



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


# UCSC MySQL interface
UCSC_HOST = "genome-euro-mysql.soe.ucsc.edu"
UCSC_USER = "genome"
UCSC_PASS = None
UCSC_PORT = 3306


# UCSC DAS server
DAS_HOST  = "http://genome.ucsc.edu/cgi-bin/das/"
DAS_QUERY = "/dna?segment="
DAS_SEPARATOR = ","


# genomic coordinates attributes of a RefSeq identifier
GENOME_BUILD = "genome build"
CHROMOSOME   = "chromosome"
TX_START = "transcription start position"
TX_END   = "transcription end position"
STRAND   = "strand"


# logger
logger = logging.getLogger("microrna.org")



#
# query UCSC via MySQL interface to retrieve the genomic location of the
# provided RefSeq identifier given its genome build as reference. Return the
# result in a Bio.SeqRecord annotated with:
# - chromosome location
# - transcription start site (1-based counting)
# - transcription end site
# - strand
#
def genomic_coordinates(refseq_id, genome):
    """
    Returns an annotated Bio.SeqRecord containing the provided RefSeq
    identifier and genome build, chromosome, transcription start/end positions
    (1-based counting) and strand.
    Relies on UCSC MySQL interface (genome.ucsc.edu/goldenpath/help/mysql.html.
    """

    query = "select g.chrom, g.txStart, g.txEnd, g.strand \
        from refGene g, knownToRefSeq r where g.name = '%s' \
        AND r.value = g.name;"%(refseq_id)

    result = None

    db = pymysql.connect(host=UCSC_HOST, port=UCSC_PORT,
        user=UCSC_USER, password=UCSC_PASS, database=genome)

    cursor = db.cursor()

    try:
        cursor.execute(query)
        data = cursor.fetchone()

        # initialize the Bio.SeqRecord object
        result = Bio.SeqRecord(seq="", id=refseq_id)

        # annotate the Bio.SeqRecord object
        result.annotations[GENOME_BUILD] = genome
        result.annotations[CHROMOSOME] = data[0]
        result.annotations[TX_START] = (data[1] + 1) # (1-based counting)
        result.annotations[TX_END] = data[2]
        result.annotations[STRAND] = data[3]

    except:
        logger.error("Unable to fetch data from UCSC Table Browser")

    db.close()

    return result



#
# update the sequence of the given Bio.SeqRecord.
# Use the UCSC DAS server (follows GenBank/EMBL 1-based counting).
#
def genomic_sequence(refseq_id_record):
    """
    Updates the provided Bio.SeqRecord object with its genomic sequence.
    Relies on UCSC DAS server (http://genome.ucsc.edu/cgi-bin/das/), which
    follows the GenBank/EMBL 1-based counting,
    """

    query = str(
        DAS_HOST + refseq_id_record.annotations[GENOME_BUILD] +
        DAS_QUERY + refseq_id_record.annotations[CHROMOSOME] +
        SEPARATOR + str(refseq_id_record.annotations[TX_START]) +
        DAS_SEPARATOR + str(refseq_id_record.annotations[TX_END]))

    result = refseq_id_record

    try:
        response = requests.get(query)

        if response.status_code == 200:

            # The UCSC DAS server wraps the genomic sequence in an XML tree
            # that looks like the following:
            #
            # <DASDNA>
            #   <SEQUENCE>
            #     <DNA>
            #     The sequence...
            #     </DNA>
            #   </SEQUENCE>
            # </DASDNA>

            # extract sequence from XML tree
            soup = BeautifulSoup(response.content, 'html.parser')

            # create a Bio.Seq object
            sequence = Seq(
                re.sub('\n', '', soup.dna.string),
                IUPAC.unambiguous_dna)

            # updated the provided Bio.SeqRecord object with the retrieved
            # sequence
            result.seq = sequence

        else:
            logger.error("Unable to retrieve sequence. DAS server returned Error code %s",
                str(response.status_code))

    except:
        logger.error("Ubable to fetch data from UCSC DAS server")

    return result


#
# return the transcript sequence of the given Bio.SeqRecord between the
# specified start and end positions (1-based counting)
#
def transcript_sequence_in_range(refseq_id_record, start, end):
    """
    Returns the transcript sequence of the provided Bio.SeqRecord that is found
    between the given range (1-based counting).
    """

    gene_start = refseq_id_record.annotations[TX_START]

    section = refseq_id_record.seq[(start - gene_start):((end - gene_start)+1)]

    return section.transcribe()



def init_ns(cache, options):
    read(cache, options)
    filtrate(cache, options)



#
# read the microrna.org target prediction file and cache all putative triplexes
#
def read(cache, options):
    """
    Reads the microrna.org target prediction file, and caches all duplexes
    within it.
    """

    count_lines    = 0
    count_duplexes = 0

    in_file = None


    # download the input file that is relative to the current namespace.
    # However, avoid downloading more than once

    ns_source = NAMESPACES[int(options[OPT_NAMESPACE])][SOURCE]

    # the requested file is within the known test data path
    # ==> use it
    if TEST_PATH in Path(ns_source).parents:

        logger.info("Using \"test data\" target prediction file " + ns_source)
        in_file = Path(ns_source)

    # the requested file is not within the known test data path
    # ==> download it, or use its local copy
    else:

        ns_file = FILE_PATH.joinpath(ns_source.split('/')[-1])

        # file is not there
        # ==> download it
        if not ns_file.is_file():

            logger.info("Downloading target prediction file from " + ns_source)
            response = requests.get(ns_source)
            if response.status_code == 200:
                with open(ns_file, 'wb') as dst:
                    dst.write(response.content)
            else:
                logger.error("Error retrieving target prediction file. Server returned "
                    + str(response.status_code))
                sys.exit(1)

        # file is there
        # ==> use it
        else:

            logger.info("Using cached target prediction file " + ns_file.name)

        in_file = ns_file


    # input namespace
    namespace = NAMESPACES[int(options[OPT_NAMESPACE])][STRING]

    logger.info("  Reading putative triplexes from microrna.org file \"%s\" ...", in_file)
    logger.info("  Namespace \"%s\"", namespace)


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
                    ":target:" +
                    target_hash[TRANSCRIPT_ID] +
                    ":duplexes"
                )

                # cache
                try:
                    # cache the dictionary representation of the current duplex
                    # in a redis hash
                    cache.hmset(duplex, target_hash)
                    logger.debug(
                        "      Cached key-value pair duplex %s with attributes from line %d",
                        duplex, count_lines
                    )

                    # cache the redis hash reference in a redis set of duplexes
                    # sharing the same target
                    cache.sadd(target_duplexes, duplex)
                    logger.debug(
                        "      Cached duplex id %s as relative to target %s",
                        duplex, target
                    )

                    # cache the target in a redis set
                    cache.sadd(targets, target)
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
        "  Found %s RNA duplexes across %s target genes",
        str(count_duplexes), str(cache.scard(targets))
    )



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
# TODO: this function must be source-agnostic, i.e. comparisons should be made
# regardless the data is from microrna.org, TargetScan, etc.
def filtrate(cache, options):
    """
    Retrieves each target and set of associated duplexes, and builds a list
    containing all possible comparisons among those duplexes whose seed-binding
    distance resides within the allowed nt. range (Saetrom et al. 2007).
    This process is carried out on multiple targets in parallel.
    """

    logger.info("  Finding allowed duplex-pair comparisons among each target's duplex ...")


    # generate all comparison jobs in parallel, assigning the same job to as
    # many processes as number of given cores
    procs = [
        Process(target=generate_allowed_comparisons, args=(cache, options, x)) for x in range(int(options[OPT_CORES]))
    ]
    [p.start() for p in procs]
    [p.join() for p in procs]



#
# generate the allowed duplex-pair comparison list
# TODO: this function must be source-agnostic, i.e. comparisons should be made
# regardless the data is from microrna.org, TargetScan, etc.
def generate_allowed_comparisons(cache, options, core):
    """
    Takes each target gene's cached duplex, and compares them all to spot
    duplexes whose miRNA binds the mutual target within the seed binding range
    outlined by Saetrom et al. (2007). This range defines a constraint for the
    formation of a putative RNA triplex. Duplex pairs that conserve this
    constraint are then cached for later statistical validation.
    """

    # caching namespace
    namespace = NAMESPACES[int(options[OPT_NAMESPACE])][STRING]

    # per-worker summary statistics
    statistics_targets = 0
    statistics_targets_with_duplex_pairs_within_range = 0
    statistics_duplex_pairs = 0
    statistics_duplex_pairs_binding_within_range = 0

    # work until there are available targets :)
    while True:

        # get the next available target, and create all duplex-pairs from its
        # associated duplex set. Regardless of the miRNA IDs (the same miRNA
        # can in fact bind the same target at different positions), test
        # whether the miRNA binding distance is within the range outlined by
        # Saetrom et al. (2007)

        target = cache.spop( (namespace + str(":targets")) )

        # (popped targets will be cached in another set to allow further
        # operations, or ignored in case they do not form any allowed RNA
        # triplex)

        if target:

            statistics_targets += 1

            logger.debug(
                "    Worker %d: Computing allowed triplexes for target %s",
                core, target)

            # compute all possible duplex-pairs

            target_duplexes = cache.smembers( (target + ":duplexes"))

            logger.debug(
                "    Worker %d:   Target found in %d duplexes",
                core, len(target_duplexes)
            )

            duplex_pairs = list(
                itertools.combinations(target_duplexes, 2)
            )

            # keep a record
            statistics_duplex_pairs += len(duplex_pairs)

            duplex_pairs_binding_within_range = 0

            logger.debug(
                "    Worker %d:   Target %s has %d duplex pairs",
                core, target, len(duplex_pairs)
            )

            for duplex_pair in duplex_pairs:

                # get the miRNA-target binding start position for duplex1
                duplex1 = duplex_pair[0]
                duplex1_alignment_start = int(
                    cache.hget(duplex1, ALIGNMENT_GENE_START)
                )
                #logger.debug(
                #    "    Worker %d:     Duplex %s aligns at %s",
                #    core, duplex1, duplex1_alignment_start
                #)

                # get the miRNA-target binding start position for duplex2
                duplex2 = duplex_pair[1]
                duplex2_alignment_start = int(
                    cache.hget(duplex2, ALIGNMENT_GENE_START)
                )
                #logger.debug(
                #    "    Worker %d:     Duplex %s aligns at %s",
                #    core, duplex2, duplex2_alignment_start
                #)

                # compute the binding distance
                binding = abs(
                    duplex1_alignment_start - duplex2_alignment_start
                )
                #logger.debug(
                #    "    Worker %d:     Duplex binding range is %s",
                #    core, binding
                #)

                # putative triplexes have their miRNAs binding a mutual target
                # gene within 13-35 seed distance range (Saetrom et al. 2007).
                # Before proper statistical validation, a candidate triplex
                # conserves this experimentally validated property.
                # ==> Test whether the binding distance is within the allowed
                # distance range, and if so, keep the duplex-pair comparison
                if (SEED_MAX_DISTANCE >= binding) and (binding >= SEED_MIN_DISTANCE):

                    logger.debug(
                        "    Worker %d:   Target %s duplex pair :%s and :%s bind within the allowed range (%d >= %d >= %d). Duplex pair kept",
                        core, target,
                        str(duplex1.split(SEPARATOR)[-1]),
                        str(duplex2.split(SEPARATOR)[-1]),
                        SEED_MAX_DISTANCE, binding, SEED_MIN_DISTANCE
                    )

                    # cache the duplex pairs whose seed site distance is within
                    # the allowed range
                    cache.lpush(
                        (target + ":with_mirna_pair_in_allowed_binding_range"),
                        duplex1
                    )
                    cache.lpush(
                        (target + ":with_mirna_pair_in_allowed_binding_range"),
                        duplex2
                    )

                    # keep a record of the number of binding-within-range
                    # duplex pairs
                    duplex_pairs_binding_within_range += 1
                    statistics_duplex_pairs_binding_within_range += 1

                else:
                    logger.debug(
                        "    Worker %d:   Target %s duplex pair :%s and :%s bind outside the allowed range. Duplex pair discarded",
                        core, target,
                        duplex1.split(SEPARATOR)[-1],
                        duplex2.split(SEPARATOR)[-1]
                    )


            logger.debug(
                "    Worker %d:   Target %s found in %d duplex pairs, of which %d comply with the allowed binding range constraint",
                core, target, len(duplex_pairs),
                duplex_pairs_binding_within_range
            )

            # cache all allowed duplex-pair comparisons
            if duplex_pairs_binding_within_range > 0:
                statistics_targets_with_duplex_pairs_within_range += 1

                # cache the popped target in a set of allowed seed
                # binding range targets
                cache.sadd((namespace + ":targets:with_mirna_pair_in_allowed_binding_range"), target)

                logger.debug(
                    "    Worker %d:   Target %s cached",
                    core, target
                )

        else:
            break

    logger.info(
        "  Worker %d: Examined %d targets and %d duplex pairs. Found %d targets with miRNA pairs binding within range, and %d putatively cooperating miRNA pairs",
        core, statistics_targets, statistics_duplex_pairs,
        statistics_targets_with_duplex_pairs_within_range,
        statistics_duplex_pairs_binding_within_range
    )

