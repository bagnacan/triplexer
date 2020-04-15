<div id="top"></div>

[![Docker Repository on Quay](https://quay.io/repository/bagnacan/triplexer/status "Docker Repository on Quay")](https://quay.io/repository/bagnacan/triplexer)

# Triplexer

The Triplexer is a computational pipeline that builds the backend database of
the [TriplexRNA](https://triplexrna.org): a database of cooperative microRNAs
and their mutual targets.  
The Triplexer is based on the work of
[Lai et al.](https://doi.org/10.1093/nar/gks657) and
[Schmitz et al.](https://doi.org/10.1093/nar/gku465), and extends it for
multiple organisms and prediction algorithms.

- [Installation requirements](#installation-requirements)
- [Usage](#usage)



## Installation requirements

The only requirement is [Docker](https://www.docker.com/), which can be
installed in different ways depending on the underlying operative system:
- Unix users should follow the [Docker installation for Linux](https://docs.docker.com/compose/install/#install-compose-on-linux-systems#install-compose-on-linux-systems),
and install both Docker and Docker compose
- MacOS 10.13+ users should follow the [Docker installation for Mac](https://docs.docker.com/docker-for-mac/install/)
- Windows 10+ users, should follow the [Docker installation for Windows](https://docs.docker.com/docker-for-windows/install/)
- For legacy systems, users can rely on the [Docker Toolbox](https://docs.docker.com/toolbox/overview/).
<p align="right"><a href="#top">&#x25B2; back to top</a></p>



## Usage

To run the Triplexer docker container and all containers it relies on, type:
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
  -s, --store           store the provided dataset (requires: -o, -n, -g, -i)
  -f, --filter          filter entries not forming putative triplexes (requires: -o, -n, -g)
  -p, --predict         predict putative triplexes
  -t, --test            test stability of predicted triplexes

target organism:
  -o ORG, --org ORG     set ORG as model organism
  -n NS, --ns NS        set NS as model organism namespace
  -g GEN, --genome GEN  set GEN as model organism genome release
  -i INPUT, --input INPUT
                        set INPUT as model organism input dataset
```

**Example**: Read microrna.org's Human (hg19) [target site predictions](http://www.microrna.org/microrna/getDownloads.do)
in memory, for later filtering for RNA triplex constraints and stability testing:
```
triplexer -s -o hsa -g hg19 -n microrna_org -i /data/human_predictions_S_C_aug2010.txt
```
<p align="right"><a href="#top">&#x25B2; back to top</a></p>
