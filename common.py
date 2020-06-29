#
# module for the common values
#


TRIPLEXER = "triplexer"
VERSION   = "0.1"

SEPARATOR = ":"
FILE_EXT_LOG = ".log"
FILE_PATH = "/tmp"
TEST_PATH = "data"



# Saetrom et al. 2007 (doi:10.1093/nar/gkm133) defined the following distance
# binding range constraint for experimentally validated RNA triplexes
#
SEED_MIN_DISTANCE = 13
SEED_MAX_DISTANCE = 35



# genomic coordinates attributes of a RefSeq identifier
#
REF_GENOME   = "genome build"
REF_CHR      = "chromosome"
REF_TX_START = "transcription start position"
REF_TX_END   = "transcription end position"
REF_STRAND   = "strand"



# supported namespaces
#
# NOTE: ADD NEW NAMESPACES IN THE FOLLOWING DICTIONARY
# - namespaces will appear in the usage instructions
# - namespace numbers will be used as a shortcut to reference their string on
#   the CLI
#
NS_LABEL    = "ns label"
NS_SOURCE   = "ns source"
NS_ORIGIN   = "ns origin"
NS_RELEASE  = "ns release"
NS_ORGANISM = "ns organism"
NS_GENOME   = "ns genome"

MICRORNA_ORG = "microrna.org"

NAMESPACES = {
    "test": {
        NS_LABEL:    str(MICRORNA_ORG + ":aug.2010:hsa:hg19"),
        NS_SOURCE:   "data/microrna.org__aug.2010__hsa__hg19.test",
        NS_ORIGIN:   MICRORNA_ORG,
        NS_RELEASE:  "aug.2010",
        NS_ORGANISM: "hsa",
        NS_GENOME:   "hg19"
    },
    "1": {
        NS_LABEL:    str(MICRORNA_ORG + ":aug.2010:hsa:hg19"),
        NS_SOURCE:   "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__hsa__hg19.tsv",
        NS_ORIGIN:   MICRORNA_ORG,
        NS_RELEASE:  "aug.2010",
        NS_ORGANISM: "hsa",
        NS_GENOME:   "hg19"
    },
    "2": {
        NS_LABEL:    str(MICRORNA_ORG + ":aug.2010:mmu:mm9"),
        NS_SOURCE:   "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__mmu__mm9.tsv",
        NS_ORIGIN:   MICRORNA_ORG,
        NS_RELEASE:  "aug.2010",
        NS_ORGANISM: "mmu",
        NS_GENOME:   "mm9"
    },
    "3": {
        NS_LABEL:    str(MICRORNA_ORG + ":aug.2010:rno:rn4"),
        NS_SOURCE:   "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__rno__rn4.tsv",
        NS_ORIGIN:   MICRORNA_ORG,
        NS_RELEASE:  "aug.2010",
        NS_ORGANISM: "rno",
        NS_GENOME:   "rn4"
    },
    "4": {
        NS_LABEL:    str(MICRORNA_ORG + ":aug.2010:dme:dm3"),
        NS_SOURCE:   "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__dme__dm3.tsv",
        NS_ORIGIN:   MICRORNA_ORG,
        NS_RELEASE:  "aug.2010",
        NS_ORGANISM: "dme",
        NS_GENOME:   "dm3"
    }
}
