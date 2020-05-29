VERSION = "0.1"

SEPARATOR = ":"


# options
OPT_ORGANISM       = "org"
OPT_ORGANISM_SHORT = str("-" + OPT_ORGANISM[:1])
OPT_ORGANISM_EXT   = str("--" + OPT_ORGANISM)
OPT_NAMESPACE       = "ns"
OPT_NAMESPACE_SHORT = str("-" + OPT_NAMESPACE[:1])
OPT_NAMESPACE_EXT   = str("--" + OPT_NAMESPACE)
OPT_GENOME       = "genome"
OPT_GENOME_SHORT = str("-" + OPT_GENOME[:1])
OPT_GENOME_EXT   = str("--" + OPT_GENOME)
OPT_INPUT       = "input"
OPT_INPUT_SHORT = str("-" + OPT_INPUT[:1])
OPT_INPUT_EXT   = str("--" + OPT_INPUT)
OPT_CORES       = "exe"
OPT_CORES_SHORT = str("-" + OPT_CORES[1:2])
OPT_CORES_EXT   = str("--" + OPT_CORES[:3])
OPT_DB       = "db"
OPT_DB_SHORT = str("-" + OPT_DB[:1])
OPT_DB_EXT   = str("--" + OPT_DB)

OPT_INIT_NS         = "bootstrap_ns"
OPT_INIT_NS_SHORT   = str("-" + OPT_INIT_NS[:1])
OPT_INIT_NS_EXT     = str("--" + OPT_INIT_NS)
OPT_INIT_NS_REQUIRE = []

OPT_READ         = "read"
OPT_READ_SHORT   = str("-" + OPT_READ[:1])
OPT_READ_EXT     = str("--" + OPT_READ)
OPT_READ_REQUIRE = [
    OPT_ORGANISM,
    OPT_NAMESPACE,
    OPT_GENOME,
    OPT_INPUT
]
OPT_READ_REQUIRE_CLI = [
    OPT_ORGANISM_SHORT,
    OPT_NAMESPACE_SHORT,
    OPT_GENOME_SHORT,
    OPT_INPUT_SHORT
]
OPT_FILTER         = "filter"
OPT_FILTER_SHORT   = str("-" + OPT_FILTER[:1])
OPT_FILTER_EXT     = str("--" + OPT_FILTER)
OPT_FILTER_REQUIRE = [
    OPT_ORGANISM,
    OPT_NAMESPACE,
    OPT_GENOME
]
OPT_FILTER_REQUIRE_CLI = [
    OPT_ORGANISM_SHORT,
    OPT_NAMESPACE_SHORT,
    OPT_GENOME_SHORT
]
OPT_PREDICT       = "predict"
OPT_PREDICT_SHORT = str("-" + OPT_PREDICT[:1])
OPT_PREDICT_EXT   = str("--" + OPT_PREDICT)
OPT_TEST       = "test"
OPT_TEST_SHORT = str("-" + OPT_TEST[:1])
OPT_TEST_EXT   = str("--" + OPT_TEST)


# option dependencies
OPTS_DEPENDENCIES = {
    OPT_INIT_NS: OPT_INIT_NS_REQUIRE,
    OPT_READ: OPT_READ_REQUIRE,
    OPT_FILTER: OPT_FILTER_REQUIRE
}

# operations and their precedence
OPS = {
    OPT_INIT_NS,
    OPT_READ,
    OPT_FILTER,
    OPT_PREDICT,
    OPT_TEST
}


# Saetrom et al. 2007 (doi:10.1093/nar/gkm133) defined the following distance
# binding range constraint for experimentally validated RNA triplexes
SEED_MIN_DISTANCE = 13
SEED_MAX_DISTANCE = 35
