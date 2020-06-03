<div id="top"></div>

[![Docker Repository on Quay](https://quay.io/repository/bagnacan/triplexer/status "Docker Repository on Quay")](https://quay.io/repository/bagnacan/triplexer)

# Triplexer

The Triplexer is a computational pipeline that builds the backend database of
the [TriplexRNA](https://triplexrna.org): a database of cooperative microRNAs
and their mutual targets.  
The pipeline is based on the work of [Lai et al.](https://doi.org/10.1093/nar/gks657)
and [Schmitz et al.](https://doi.org/10.1093/nar/gku465), and extended to
cover multiple organisms and prediction algorithms.

- [Installation requirements](#installation-requirements)
- [Run the Triplexer](#run-the-triplexer)
  - [Operation read](#operation-read)
  - [Operation filter](#operation-filter)



## Installation requirements

The only requirement is [Docker](https://www.docker.com/), which can be
installed in different ways depending on the underlying operative system:
- Unix users should follow the [Docker installation for Linux](https://docs.docker.com/compose/install/#install-compose-on-linux-systems#install-compose-on-linux-systems),
and install both Docker and Docker compose
- MacOS 10.13+ users should follow the [Docker installation for Mac](https://docs.docker.com/docker-for-mac/install/)
- Windows 10+ users, should follow the [Docker installation for Windows](https://docs.docker.com/docker-for-windows/install/)
- For legacy systems, users can rely on the [Docker Toolbox](https://docs.docker.com/toolbox/overview/).
<p align="right"><a href="#top">&#x25B2; back to top</a></p>



## Run the Triplexer

To run the Triplexer pipeline, you need to run the Triplexer docker container
and all containers it relies on. Type:
```
docker-compose run triplexer
```

You can now launch the Triplexer pipeline. Try it with no arguments to overview
its command line options:
```
$ triplexer
usage: triplexer [-h] [-v] [-c CONF] [-x CORES] [-d DB] [-i] [-r] [-f] [-p] [-t] [-n NS]

Predict and simulate putative RNA triplexes.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print the version and exit
  -c CONF, --conf CONF  set CONF as configuration file
  -x CORES, --exe CORES
                        set CORES as number of parallel processes
  -d DB, --db DB        set DB as intermediate results database

operations (require -n):
  -i, --init_ns         initialize the cache with putative RNA triplexes
                        (same as -r -f)
  -r, --read            read the provided dataset in memory
  -f, --filtrate        filter entries not forming putative triplexes
  -p, --predict         predict putative triplexes
  -t, --test            test stability of predicted triplexes

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

The Triplexer command line interface defines three operations, which allow for
the creation of the multi-organism backend database of the [TriplexRNA](https://triplexrna.org).
<p align="right"><a href="#top">&#x25B2; back to top</a></p>



### Operation read

The *read* operation parses the provided RNA duplexes, and creates a cache
that is used to find putative RNA triplexes.  

In a microrna.org file, each line represent an RNA *duplex*. These are
carachterized by:
- a gene target identifier,
- a miRNA identifier,
- a set of attributes related to the biological complex.

Multiple lines can refer to the same target gene. For this reason, the read
operation reads the provided input only once, and organizes the parsed duplex
information as follows:
- *targets*  
A set that stores the gene target identifiers
- *target*  
A value that represents a target identifier
- *duplex*  
A hash that stores the duplex details found at some line
- *target_duplexes*  
A set that stores the duplexes targeting some target

So, for example, the set *targets* that registers all *target* identifiers will
look like:
```
microrna_org:aug2010:hsa:hg19:targets
|- microrna_org:aug2010:hsa:hg19:target:uc001zmx.1
|- microrna_org:aug2010:hsa:hg19:target:uc001ulh.2
|- microrna_org:aug2010:hsa:hg19:target:uc010zln.1
|- ...
```

The set *target_duplex* of target ``uc001zmx.1`` that stores all duplex entries
targeting ``uc001zmx.1`` will look like:
```
microrna_org:aug2010:hsa:hg19:target:uc001zmx.1:duplexes
|- microrna_org:aug2010:hsa:hg19:duplex:line524
|- ...
```
While the set *target_duplex* of target ``uc001ulh.2`` that stores all duplex
targeting ``uc001ulh.2`` will look like:
```
microrna_org:aug2010:hsa:hg19:target:uc001ulh.2:duplexes
|- microrna_org:aug2010:hsa:hg19:duplex:line277
|- ...
```

And so on.  

**Example**: Create a cache of microrna.org's Human hg19 [target site predictions](http://www.microrna.org/microrna/getDownloads.do)
to find putative RNA triplexes:
```
triplexer -r
```

<p align="right"><a href="#top">&#x25B2; back to top</a></p>



### Operation filter

Experimental findings suggest that RNA triplexes form when two cooperating
miRNAs bind a common target with a seed site distance between 13 and 35
nucleotides [(Saetrom et al. 2007)](https://doi.org/10.1093/nar/gkm133).
This means that among those cached duplexes that share a common target, there
might also some that do not comply with the aforementioned seed site distance
constraint.  
The *filter* operation takes all duplexes targeting some gene, creates an index
of all possible duplex pairs, and discards those that do not comply with the
constraint.  

This operation relies on the cache created by the read operation (see above).  
With reference to the names defined in the [operation read](#operation-read)
section, the filter's behavior can be summarized by the following pseudo-code:
```
for each target in the set of targets:
    for each duplex in the set of target_duplexes:
        if duplex pair has miRNA alignment within binding range constraint:
            cache the target
            cache the duplex pair
```

**Example**: Filter the cached duplexes to retain only those whose miRNA bind a
common target within the allowed binding distance range:
```
triplexer -f
```
<p align="right"><a href="#top">&#x25B2; back to top</a></p>
