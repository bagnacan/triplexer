#
# module for managing data retrieval operations in the UCSC
#


import logging
import pymysql
import re
import requests
from bs4 import BeautifulSoup
from common import *
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC


# UCSC MySQL interface
UCSC_HOST = "genome-euro-mysql.soe.ucsc.edu"
UCSC_USER = "genome"
UCSC_PASS = None
UCSC_PORT = 3306


# UCSC DAS server
DAS_HOST  = "http://genome.ucsc.edu/cgi-bin/das/"
DAS_QUERY = "/dna?segment="
DAS_SEPARATOR = ","


# genomic attributes of a RefSeq identifier
#ID = "gene RefSeq ID"
#SEQUENCE = "gene sequence"


# logger
logger = logging.getLogger("UCSC")



# query the UCSC via MySQL interface to retrieve the genomic location of the
# provided Bio.SeqRecord, given its RefSeq ID and genome build annotation.
# Return the updated record as result. Updates are found in its annotations:
# - chromosome location
# - transcription start site (1-based counting)
# - transcription end site
# - strand
#
def genomic_coordinates(bio_seq, core):
    """
    Returns an updated Bio.SeqRecord containing the provided RefSeq identifier
    and genome build, chromosome, transcription start/end positions (1-based
    counting) and strand.
    Relies on UCSC MySQL interface (genome.ucsc.edu/goldenpath/help/mysql.html).
    """

    query = "select g.chrom, g.txStart, g.txEnd, g.strand \
        from refGene g, knownToRefSeq r where g.name = '%s' \
        AND r.value = g.name;"%(bio_seq.id)

    result = None

    db = pymysql.connect(host=UCSC_HOST, port=UCSC_PORT,
        user=UCSC_USER, password=UCSC_PASS,
        database=bio_seq.annotations[GENOME_BUILD])

    cursor = db.cursor()

    try:
        cursor.execute(query)
        data = cursor.fetchone()

        # initialize the Bio.SeqRecord object
        result = bio_seq

        # update the annotations of the given Bio.SeqRecord object
        result.annotations[CHROMOSOME] = data[0]
        result.annotations[TX_START] = (data[1] + 1) # (1-based counting)
        result.annotations[TX_END] = data[2]
        result.annotations[STRAND] = data[3]

        logger.debug("  Worker %d:   Retrieved genomic location of target %s from UCSC",
            core, bio_seq.id)

    except:
        logger.debug("  Worker %d:   Unable to fetch the genomic location of target %s from UCSC",
            core, bio_seq.id)

    db.close()

    return result



# update the sequence of the given Bio.SeqRecord.
# Use the UCSC DAS server (follows GenBank/EMBL 1-based counting).
#
def genomic_sequence(bio_seq, core):
    """
    Updates the provided Bio.SeqRecord object with its genomic sequence.
    Relies on UCSC DAS server (http://genome.ucsc.edu/cgi-bin/das/), which
    follows the GenBank/EMBL 1-based counting,
    """

    query = str(
        DAS_HOST + bio_seq.annotations[GENOME_BUILD] +
        DAS_QUERY + bio_seq.annotations[CHROMOSOME] +
        SEPARATOR + str(bio_seq.annotations[TX_START]) +
        DAS_SEPARATOR + str(bio_seq.annotations[TX_END]))

    result = None

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
            bio_seq.seq = sequence

            logger.debug("  Worker %d:   Retrieved genomic sequence of target %s from DAS server",
                core, bio_seq.id)

            result = bio_seq

        else:
            logger.debug("  Worker %d:   Unable to fetch the genomic sequence of target %s. DAS server returned Error code %s",
                core, bio_seq.id, str(response.content))

    except:
        logger.error("Ubable to fetch data from UCSC DAS server")

    return result



# return the transcript sequence of the given Bio.SeqRecord between the
# specified start and end positions (1-based counting)
#
def transcript_sequence_in_range(bio_seq, start, end):
    """
    Returns the transcript sequence of the provided Bio.SeqRecord that is found
    between the given range (1-based counting).
    """

    gene_start = bio_seq.annotations[TX_START]

    section = bio_seq.seq[(start - gene_start):((end - gene_start)+1)]

    return section.transcribe()



## return a dictionary representation of the current Bio.SeqRecord
##
#def bio_seq2dict(bio_seq):
#    """
#    Returns a dictionary representation of the given Bio.SeqRecord.
#    """
#
#    # build a dictionary representation from all fields in the Bio.SeqRecord
#    result = {
#        ID         : bio_seq.id,
#        SEQUENCE   : bio_seq.sequence,
#        CHROMOSOME : bio_seq.annotations[CHROMOSOME],
#        TX_START   : bio_seq.annotations[TX_START],
#        TX_END     : bio_seq.annotations[TX_END],
#        STRAND     : bio_seq.annotations[STRAND]
#    }
#
#    return result

