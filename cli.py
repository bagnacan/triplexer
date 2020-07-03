#
# command line module
#


import argparse
from common import *



# system setting arguments
#
OPT_NAMESPACE       = "ns"
OPT_NAMESPACE_SHORT = str("-" + OPT_NAMESPACE[:1])
OPT_NAMESPACE_EXT   = str("--" + OPT_NAMESPACE)
OPT_EXE       = "exe"
OPT_EXE_SHORT = str("-" + OPT_EXE[:1])
OPT_EXE_EXT   = str("--" + OPT_EXE[:])
OPT_DB       = "db"
OPT_DB_SHORT = str("-" + OPT_DB[:1])
OPT_DB_EXT   = str("--" + OPT_DB)


# operation arguments
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

# annotate
OPT_ANNOTATE         = "annotate"
OPT_ANNOTATE_SHORT   = str("-" + OPT_ANNOTATE[:1])
OPT_ANNOTATE_EXT     = str("--" + OPT_ANNOTATE)

# all operations
#
# NOTE: ADD NEW NAMESPACES-SPECIFIC-OPERATIONS IN THE FOLLOWING DICTIONARY
# The triplexer identifies 3 abstract operations:
# - read        for reading an input file containing miRNA duplexes
# - filtrate    for keeping only those miRNA duplexes that bind a common target
#               gene in compliance with defined structural constraints
# - annotate    to retrieve the target gene's transcript sequence from a remote
#               database
# Since the identification of putative RNA triplexes is carried out by
# harvesting data from different sources (namespace, e.g. microrna.org,
# TargetScan, etc.), it is safe to assume that input datasets have a different
# organization, i.e. duplex information in a microrna.org file are not the same
# as those found in a TargetScan dataset. Hence, the implementation and
# combination of each operations is "namespace-specific".
# For example, to find putative RNA triplexes in a microrna.org dataset, one
# needs to run:
# - a namespace-specific implementation of the operation read
# - a namespace-agnostic implementation of the operation filtrate
# - a namespace-agnostic implementation of the operation annotate
# However, to find putative RNA triplexes from a different namespace, one might
# need to instead run:
# - a namespace-specific implementation of the operation read
# - the same namespace-agnostic implementation of the operation filtrate
# - no operation annotate
# For this reason, we collect the set of all namespace-specific-operations
# in the following dictionary
OPS = {
    MICRORNA_ORG: [
        OPT_INIT_NS,
        OPT_READ,
        OPT_FILTRATE,
        OPT_ANNOTATE
    ]
}



# set the CLI parser
#
def triplexer_parser():
    """
    Sets the command line (CLI) parser.
    """

    # system setting arguments start
    #
    parser = argparse.ArgumentParser(
        prog=TRIPLEXER,
        description="Predict and simulate putative RNA triplexes.",
        formatter_class=argparse.RawTextHelpFormatter)

    # version
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=str("%(prog)s " + VERSION),
        help="print the version and exit")

    # configuration file
    parser.add_argument(
        "-c",
        "--conf",
        metavar="CONF",
        default="conf.yaml",
        type=argparse.FileType("r"),
        help="set %(metavar)s as configuration file")

    # cores
    parser.add_argument(
        OPT_EXE_SHORT,
        OPT_EXE_EXT,
        metavar="EXE",
        default="2",
        help="set %(metavar)s as number of parallely executing processes")

    # cache
    parser.add_argument(
        OPT_DB_SHORT,
        OPT_DB_EXT,
        metavar="DB",
        default="redis:6379",
        help="set %(metavar)s as intermediate results database")
    #
    # system setting arguments end


    # operation arguments start
    #
    parser_op = parser.add_argument_group("operations (require "
        + OPT_NAMESPACE_SHORT + ")")

    parser_op.add_argument(
        OPT_READ_SHORT,
        OPT_READ_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help=str("read the provided dataset in memory"))

    parser_op.add_argument(
        OPT_FILTRATE_SHORT,
        OPT_FILTRATE_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help=str("filter entries not forming putative triplexes"))

    parser_op.add_argument(
        OPT_ANNOTATE_SHORT,
        OPT_ANNOTATE_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help=str("annotate transcripts with their sequences"))

    parser_op.add_argument(
        OPT_INIT_NS_SHORT,
        OPT_INIT_NS_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help=str("initialize the cache with putative RNA triplexes\n"
            + "(same as " + " ".join( str(x) for x in OPT_INIT_NS_SAME_AS_CLI)
            + ")"))
    #
    # operation arguments end


    # namespace arguments start
    #
    supported_namespaces = get_supported_namespaces() # supported namespaces

    parser_ns = parser.add_argument_group("namespace")
    parser_ns.add_argument(
        OPT_NAMESPACE_SHORT,
        OPT_NAMESPACE_EXT,
        metavar="NS",
        default="test",
        help=str("set %(metavar)s as model organism namespace\n"
            + "supported %(metavar)s (default \"%(default)s\"):\n"
            + supported_namespaces))
    #
    # namespace arguments end

    return parser



# print the supported namespaces
#
def get_supported_namespaces():
    """
    Prints the supported namespaces.
    """

    line_divider = "+-------+----------------------------------+\n"

    supported_namespaces = line_divider

    supported_namespaces += str("|  {:<1}\t| {:<32} |\n".format(
        "NS", "database:version:organism:genome"))

    supported_namespaces += line_divider

    for k, v in NAMESPACES.items():
        label, source, origing, release, orgagnism, genome = v
        supported_namespaces += "|  {:<1}\t| {:<32} |\n".format(k, v[NS_LABEL])

    supported_namespaces += line_divider

    return supported_namespaces
