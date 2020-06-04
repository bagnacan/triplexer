#
# command line module
#


import argparse
from common import *



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
        OPT_CORES_SHORT,
        OPT_CORES_EXT,
        metavar="CORES",
        default="2",
        help="set %(metavar)s as number of parallel processes")

    # cache
    parser.add_argument(
        OPT_DB_SHORT,
        OPT_DB_EXT,
        metavar="DB",
        default="redis:6379",
        help="set %(metavar)s as intermediate results database")
    #
    # system setting arguments end


    # option arguments start
    #
    parser.add_argument_group("operations (require "
        + OPT_NAMESPACE_SHORT + ")")

    parser.add_argument(
        OPT_INIT_NS_SHORT,
        OPT_INIT_NS_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help=str("initialize the cache with putative RNA triplexes\n"
            + "(same as " + " ".join( str(x) for x in OPT_INIT_NS_SAME_AS_CLI)
            + ")"))

    parser.add_argument(
        OPT_READ_SHORT,
        OPT_READ_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help=str("read the provided dataset in memory"))

    parser.add_argument(
        OPT_FILTRATE_SHORT,
        OPT_FILTRATE_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help=str("filter entries not forming putative triplexes"))

    parser.add_argument(
        OPT_PREDICT_SHORT,
        OPT_PREDICT_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help="predict putative triplexes")

    parser.add_argument(
        OPT_TEST_SHORT,
        OPT_TEST_EXT,
        action="store_true",
        default=argparse.SUPPRESS,
        help="test stability of predicted triplexes")
    #
    # option arguments end


    # namespace arguments start
    #
    supported_namespaces = get_supported_namespaces() # supported namespaces

    parser.add_argument_group("namespace")
    parser.add_argument(
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

