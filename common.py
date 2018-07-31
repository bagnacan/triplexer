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
OPT_FILE       = "file"
OPT_FILE_SHORT = str("-" + OPT_FILE[:1])
OPT_FILE_EXT   = str("--" + OPT_FILE)
OPT_CORES       = "exe"
OPT_CORES_SHORT = str("-" + OPT_CORES[1:2])
OPT_CORES_EXT   = str("--" + OPT_CORES[:3])
OPT_LOCATION       = "location"
OPT_LOCATION_SHORT = str("-" + OPT_LOCATION[:1])
OPT_LOCATION_EXT   = str("--" + OPT_LOCATION)
OPT_LOCATION_DB       = "db"
OPT_LOCATION_DB_SHORT = str("-" + OPT_LOCATION_DB[:1])
OPT_LOCATION_DB_EXT   = str("--" + OPT_LOCATION_DB)
OPT_CACHE             = "cache"
OPT_CACHE_SHORT       = str("-" + OPT_CACHE[:1])
OPT_CACHE_EXT         = str("--" + OPT_CACHE)
OPT_CACHE_REQUIRE     = [
    OPT_ORGANISM,
    OPT_NAMESPACE,
    OPT_GENOME,
    OPT_FILE
]
OPT_CACHE_REQUIRE_CLI = [
    OPT_ORGANISM_SHORT,
    OPT_NAMESPACE_SHORT,
    OPT_GENOME_SHORT,
    OPT_FILE_SHORT
]
OPT_ALLOWED             = "allowed"
OPT_ALLOWED_SHORT       = str("-" + OPT_ALLOWED[:1])
OPT_ALLOWED_EXT         = str("--" + OPT_ALLOWED)
OPT_ALLOWED_REQUIRE     = [
    OPT_ORGANISM,
    OPT_NAMESPACE,
    OPT_GENOME,
    OPT_FILE
]
OPT_ALLOWED_REQUIRE_CLI = [
    OPT_ORGANISM_SHORT,
    OPT_NAMESPACE_SHORT,
    OPT_GENOME_SHORT
]
OPT_PREDICT       = "predict"
OPT_PREDICT_SHORT = str("-" + OPT_PREDICT[:1])
OPT_PREDICT_EXT   = str("--" + OPT_PREDICT)
OPT_SIMULATE       = "simulate"
OPT_SIMULATE_SHORT = str("-" + OPT_SIMULATE[:1])
OPT_SIMULATE_EXT   = str("--" + OPT_SIMULATE)


# option dependencies
OPTS_DEPENDENCIES = {
    OPT_CACHE: OPT_CACHE_REQUIRE,
    OPT_ALLOWED: OPT_ALLOWED_REQUIRE
}


# Saetrom et al. 2007 (doi:10.1093/nar/gkm133) defined the following distance
# binding range constraint for experimentally validated RNA triplexes
SEED_MIN_DISTANCE = 13
SEED_MAX_DISTANCE = 35
