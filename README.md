<div id="top"></div>

[![Docker Repository on Quay](https://quay.io/repository/bagnacan/triplexer/status "Docker Repository on Quay")](https://quay.io/repository/bagnacan/triplexer)

# Triplexer

The Triplexer is the computational pipeline that builds the backend database of
the [TriplexRNA](https://triplexrna.org): a database of cooperative microRNAs
and their mutual targets.  
The pipeline is based on the work of [Lai et al.](https://doi.org/10.1093/nar/gks657)
and [Schmitz et al.](https://doi.org/10.1093/nar/gku465), and extended to cover
multiple organisms and prediction algorithms.

- [Installation requirements](#installation-requirements)
- [Operations](#operations)
  - [Read duplexes](#read-duplexes)
  - [Filtrate duplexes](#filtrate-duplexes)
- [Run the Triplexer](#run-the-triplexer)
  - [Examples](#examples)



## Installation requirements

The only requirement is [Docker](https://www.docker.com/), which can be
installed in different ways depending on the underlying operative system:
- Unix users should follow the [Docker installation for Linux](https://docs.docker.com/compose/install/#install-compose-on-linux-systems#install-compose-on-linux-systems),
and install both Docker and Docker compose
- MacOS 10.13+ users should follow the [Docker installation for Mac](https://docs.docker.com/docker-for-mac/install/)
- Windows 10+ users, should follow the [Docker installation for Windows](https://docs.docker.com/docker-for-windows/install/)
- For legacy systems, users can rely on the [Docker Toolbox](https://docs.docker.com/toolbox/overview/).

<p align="right"><a href="#top">&#x25B2; back to top</a></p>



## Operations

The Triplexer defines three operations: _read_, _filtrate_, and _annotate_;
each of which is referred to a _namespace_, _i.e._ a resource (file, database,
etc.) that describes the RNA duplexes of a specific organism.  
Namespaces are used to capture the provenance of a predicted RNA duplex, and
subsequently keep the identification of putative RNA triplexes consistent
across different organisms and genome releases.

<p align="right"><a href="#top">&#x25B2; back to top</a></p>



### Read duplexes

This operation parses a file (or queries a database) containing the attributes
of a set of organism-specific RNA duplexes, and stores their attributes in the
underlying Redis cache as a set of hashes.  
Since each namespace defines its own data structures, identifiers, and
granularity of data, this operation is likely to be redefined by each
namespace. However, output data structures share a common schema regardless of
their namespace of origin. For instance, each RNA duplex is identified by the
unique string:
```
<namespace label>:<dataset release>:<organism>:<genome build>:target:<target id>
```

#For more information about a namespace-specific read implementation, please
#refer to the [IMPLEMENTATIONS.md](https://github.com/sbi-rostock/triplexer/blob/master/IMPLEMENTATIONS.md).

<p align="right"><a href="#top">&#x25B2; back to top</a></p>



### Filtrate duplexes

Experimental findings suggest that RNA triplexes form when two cooperating
miRNAs bind a common target gene with a seed site distance between 13 and 35
nucleotides [(Saetrom et al. 2007)](https://doi.org/10.1093/nar/gkm133).
This means that duplex pairs that share a common target must be tested for
complying with the aforementioned seed site distance.
constraint.  
Filtrate relies on the read operation (see above). It compares all the cached
duplexes that share a common target gene, and keeps those pairs that comply
with the seed site distance constraint. This operation is namespace agnostic.
Its behavior can be summarized by the following pseudo-code:
```
for each target in the set of targets:
    for each duplex in the set of the target's duplexes:
        if duplex pair has miRNA alignment within binding range constraint:
            cache the target
            cache the duplex pair
```

<p align="right"><a href="#top">&#x25B2; back to top</a></p>



## Run the Triplexer

To run the Triplexer pipeline, you need to run the Triplexer docker container
and all containers it relies on. This is done via docker compose. Type:
```
docker-compose run triplexer
```

You can now launch the Triplexer pipeline. Try it with no arguments to overview
its command line options:
```
$ triplexer
usage: triplexer [-h] [-v] [-c CONF] [-e EXE] [-d DB] [-r] [-f] [-a] [-n NS]

Predict and simulate putative RNA triplexes.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print the version and exit
  -c CONF, --conf CONF  set CONF as configuration file
  -e EXE, --exe EXE     set EXE as number of parallely executing processes
  -d DB, --db DB        set DB as intermediate results database

operations (require -n):
  -r, --read            read the provided dataset in memory
  -f, --filtrate        filter entries not forming putative triplexes
  -a, --annotate        annotate transcripts with their sequences

namespace:
  -n NS, --ns NS        set NS as model organism namespace
                        supported NS (default "test"):
                        +-------+----------------------------------+
                        |  NS   | database:version:organism:genome |
                        +-------+----------------------------------+
                        |  test | microrna.org:aug.2010:hsa:hg19   |
                        |  1    | microrna.org:aug.2010:hsa:hg19   |
                        |  2    | microrna.org:aug.2010:mmu:mm9    |
                        |  3    | microrna.org:aug.2010:rno:rn4    |
                        |  4    | microrna.org:aug.2010:dme:dm3    |
                        +-------+----------------------------------+
```

<p align="right"><a href="#top">&#x25B2; back to top</a></p>



### Examples

Read microrna.org's Human hg19 [target site predictions](http://www.microrna.org/microrna/getDownloads.do):
```
triplexer -n 1 -r
```

Filtrate all microrna.org's duplexes by keeping those whose miRNA pairs bind a
common target gene within the allowed distance range. Do so using 4 parallel
processes:
```
triplexer -e 4 -n 1 -f
```

<p align="right"><a href="#top">&#x25B2; back to top</a></p>

