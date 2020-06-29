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
GENOME_BUILD = "genome build"
CHROMOSOME   = "chromosome"
TX_START = "transcription start position"
TX_END   = "transcription end position"
STRAND   = "strand"



# supported namespaces
#
# ADD NEW NAMESPACES IN THE FOLLOWING DICTIONARY
# - namespaces will appear in the usage instructions
# - namespace numbers will be used as a shortcut to reference their string on
#   the CLI
#
STRING = "string"
SOURCE = "source"
ORIGIN   = "origin"
RELEASE  = "release"
ORGANISM = "organism"
GENOME   = "genome"

MICRORNA_ORG = "microrna.org"

NAMESPACES = {
    "test": {
        STRING: str(MICRORNA_ORG + ":aug.2010:hsa:hg19"),
        SOURCE: "data/microrna.org__aug.2010__hsa__hg19.test",
        ORIGIN: MICRORNA_ORG,
        RELEASE:  "aug.2010",
        ORGANISM: "hsa",
        GENOME:   "hg19"
    },
    "1": {
        STRING: str(MICRORNA_ORG + ":aug.2010:hsa:hg19"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__hsa__hg19.tsv",
        ORIGIN: MICRORNA_ORG,
        RELEASE:  "aug.2010",
        ORGANISM: "hsa",
        GENOME:   "hg19"
    },
    "2": {
        STRING: str(MICRORNA_ORG + ":aug.2010:mmu:mm9"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__mmu__mm9.tsv",
        ORIGIN: MICRORNA_ORG,
        RELEASE:  "aug.2010",
        ORGANISM: "mmu",
        GENOME:   "mm9"
    },
    "3": {
        STRING: str(MICRORNA_ORG + ":aug.2010:rno:rn4"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__rno__rn4.tsv",
        ORIGIN: MICRORNA_ORG,
        RELEASE:  "aug.2010",
        ORGANISM: "rno",
        GENOME:   "rn4"
    },
    "4": {
        STRING: str(MICRORNA_ORG + ":aug.2010:dme:dm3"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__dme__dm3.tsv",
        ORIGIN: MICRORNA_ORG,
        RELEASE:  "aug.2010",
        ORGANISM: "dme",
        GENOME:   "dm3"
    }
}
