<div id="top"></div>

[![Docker Repository on Quay](https://quay.io/repository/bagnacan/triplexer/status "Docker Repository on Quay")](https://quay.io/repository/bagnacan/triplexer)

# Triplexer

The Triplexer is a computational pipeline that builds the backend database of
the [TriplexRNA](https://triplexrna.org): a database of cooperative microRNAs
and their mutual targets.  
The Triplexer is based on the work of [Lai et al.](https://doi.org/10.1093/nar/gks657)
and [Schmitz et al.](https://doi.org/10.1093/nar/gku465), and extends it for
multiple organisms and prediction algorithms.

- [Installation requirements](#installation-requirements)
- [Run the triplexer](#run-the-triplexer)
  - [Operation read](#operation-read)
  - [Operation filter](#filter-for-binding-distance-constraint)



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
usage: triplexer [-h] [-v] [-c CONF] [-x CORES] [-d DB] [-s] [-f] [-p] [-t] [-o ORG] [-n NS] [-g GEN] [-i INPUT]

Predict and simulate putative RNA triplexes.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print the version and exit
  -c CONF, --conf CONF  set CONF as configuration file (default: conf.yaml)
  -x CORES, --exe CORES
                        set CORES as number of parallel processes (default: 2)
  -d DB, --db DB        set DB as intermediate results database (default: redis:6379)

operations:
  -r, --read            read the provided dataset in memory (requires: -o, -n, -g, -i)
  -f, --filter          filter entries not forming putative triplexes (requires: -o, -n, -g)
  -t, --test            test stability of predicted triplexes

target organism:
  -o ORG, --org ORG     set ORG as model organism
  -n NS, --ns NS        set NS as model organism namespace
  -g GEN, --genome GEN  set GEN as model organism genome release
  -i INPUT, --input INPUT
                        set INPUT as model organism input dataset
```

The Triplexer command line interface defines three operations that allow the
creation of the multi-organism backend database of the [TriplexRNA](triplexrna.org).
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
triplexer -r -o hsa -n microrna_org -g hg19 -i /data/human_predictions_S_C_aug2010.txt
```

<p align="right"><a href="#top">&#x25B2; back to top</a></p>

### Operation filter
<p align="right"><a href="#top">&#x25B2; back to top</a></p>
