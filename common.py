#
# module for the common values
#

from pathlib import Path


VERSION = "0.1"
SEPARATOR = ":"
FILE_EXT_LOG = ".log"
FILE_PATH = Path("/tmp")
TEST_PATH = Path("data")



# Saetrom et al. 2007 (doi:10.1093/nar/gkm133) defined the following distance
# binding range constraint for experimentally validated RNA triplexes
#
SEED_MIN_DISTANCE = 13
SEED_MAX_DISTANCE = 35



# supported namespaces
#
# ADD NEW NAMESPACES IN THE FOLLOWING DICTIONARY
# - namespaces will appear in the usage instructions
# - namespace numbers will be used as a shortcut to reference their string on
#   the CLI
#
STRING = "string"
SOURCE = "source"
MICRORNA_ORG = "microrna.org"
NAMESPACES = {
    "test": {
        STRING: str(MICRORNA_ORG + ":aug.2010:hsa:hg19"),
        SOURCE: "data/microrna.org__aug.2010__hsa__hg19.test"
    },
    "1": {
        STRING: str(MICRORNA_ORG + ":aug.2010:hsa:hg19"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__hsa__hg19.tsv"
    },
    "2": {
        STRING: str(MICRORNA_ORG + ":aug.2010:mmu:mm9"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__mmu__mm9.tsv"
    },
    "3": {
        STRING: str(MICRORNA_ORG + ":aug.2010:rno:rn4"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__rno__rn4.tsv"
    },
    "4": {
        STRING: str(MICRORNA_ORG + ":aug.2010:dme:dm3"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__dme__dm3.tsv"
    }
}

