#
# module for the common values
#

from pathlib import Path


VERSION = "0.1"

SEPARATOR = ":"
FILE_PATH = Path("/tmp")
TEST_PATH = Path("data")

STRING = "string"
SOURCE = "source"



# supported namespaces
#
# ADD NEW NAMESPACES IN THE FOLLOWING DICTIONARY
# - namespaces will appear in the usage instructions
# - namespace numbers will be used as a shortcut to reference their string on
#   the CLI
#
MICRORNA_ORG = "microrna.org"
NAMESPACES = {
    0: {
        STRING: str(MICRORNA_ORG + ":aug.2010:hsa:hg19"),
        SOURCE: "data/microrna.org__aug.2010__hsa__hg19.test"
    },
    1: {
        STRING: str(MICRORNA_ORG + ":aug.2010:hsa:hg19"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__hsa__hg19.tsv"
    },
    2: {
        STRING: str(MICRORNA_ORG + ":aug.2010:mmu:mm9"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__mmu__mm9.tsv"
    },
    3: {
        STRING: str(MICRORNA_ORG + ":aug.2010:rno:rn4"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__rno__rn4.tsv"
    },
    4: {
        STRING: str(MICRORNA_ORG + ":aug.2010:dme:dm3"),
        SOURCE: "https://zenodo.org/record/3870932/files/microrna.org__aug.2010__dme__dm3.tsv"
    }
}

# print the supported namespaces
#
def get_supported_namespaces():
    """
    Prints the supported namespaces.
    """

    line_divider = "+----+-------------------------------------+\n"

    supported_namespaces = line_divider

    supported_namespaces += str("| {:<2} | {:<35} |\n".format(
        "NS", "database:version:organism:genome")
    )

    supported_namespaces += line_divider

    for k, v in NAMESPACES.items():
        label, num = v
        supported_namespaces += "| {:<2} | {:<35} |\n".format(k, v[STRING])

    supported_namespaces += line_divider

    return supported_namespaces



# options
OPT_NAMESPACE       = "ns"
OPT_NAMESPACE_SHORT = str("-" + OPT_NAMESPACE[:1])
OPT_NAMESPACE_EXT   = str("--" + OPT_NAMESPACE)
OPT_CORES       = "exe"
OPT_CORES_SHORT = str("-" + OPT_CORES[1:2])
OPT_CORES_EXT   = str("--" + OPT_CORES[:3])
OPT_DB       = "db"
OPT_DB_SHORT = str("-" + OPT_DB[:1])
OPT_DB_EXT   = str("--" + OPT_DB)



# operations
#

# read
OPT_READ         = "read"
OPT_READ_SHORT   = str("-" + OPT_READ[:1])
OPT_READ_EXT     = str("--" + OPT_READ)

# filtrate
OPT_FILTRATE         = "filtrate"
OPT_FILTRATE_SHORT   = str("-" + OPT_FILTRATE[:1])
OPT_FILTRATE_EXT     = str("--" + OPT_FILTRATE)

# init namespaces
OPT_INIT_NS         = "init_ns"
OPT_INIT_NS_SHORT   = str("-" + OPT_INIT_NS[:1])
OPT_INIT_NS_EXT     = str("--" + OPT_INIT_NS)
OPT_INIT_NS_SAME_AS = [
    OPT_READ,
    OPT_FILTRATE
]
OPT_INIT_NS_SAME_AS_CLI = [
    OPT_READ_SHORT,
    OPT_FILTRATE_SHORT
]

# predict
OPT_PREDICT       = "predict"
OPT_PREDICT_SHORT = str("-" + OPT_PREDICT[:1])
OPT_PREDICT_EXT   = str("--" + OPT_PREDICT)

# test
OPT_TEST       = "test"
OPT_TEST_SHORT = str("-" + OPT_TEST[:1])
OPT_TEST_EXT   = str("--" + OPT_TEST)

# all operations
OPS = [
    OPT_INIT_NS,
    OPT_READ,
    OPT_FILTRATE,
    OPT_PREDICT,
    OPT_TEST
]



# Saetrom et al. 2007 (doi:10.1093/nar/gkm133) defined the following distance
# binding range constraint for experimentally validated RNA triplexes
#
SEED_MIN_DISTANCE = 13
SEED_MAX_DISTANCE = 35
