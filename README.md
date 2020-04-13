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
- Unix users should follow the
[Docker installation for Linux](https://docs.docker.com/installation), or rely
on their distribution's instructions
- MacOS 10.12+ users should follow the
[Docker installation for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
- Windows 10+ users, should follow the
[Docker installation for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- Non-unix users, whose operative system version is older than the
aforementioned ones, can rely on [Kitematic](https://kitematic.com/)
<p align="right"><a href="#top">&#x25B2; back to top</a></p>



## Usage

Move to the directory that stores the data that you want to analyze using the
Triplexer pipeline, then run:
```
docker run -it -v $(pwd):/data quay.io/bagnacan/triplexer:latest
```

This command runs the Triplexer docker container, and bind-mounts your
directory to the ``/data`` directory that is within the running container. This
means that you are be able to see your data by issuing ``ls -l`` in the command
line prompt.

You can now run the Triplexer. Launch it with no arguments to check its command
line options:
```
$ ./triplexer

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print the version and exit
  -c CONF, --conf CONF  set CONF as configuration file (default: conf.yaml)
  -x CORES, --exe CORES
                        set CORES as number of parallel processes (default: 2)
  -d DB, --db DB        set DB as intermediate results database (default: 127.0.0.1:6379)

target organism data:
  -o ORG, --org ORG     set ORG as model organism
  -n NS, --ns NS        set NS as model organism namespace
  -g GEN, --genome GEN  set GEN as model organism genome release
  -i INPUT, --input INPUT
                        set INPUT as model organism input dataset

operations:
  -s, --store           store the provided dataset (requires: -o, -n, -g, -i)
  -f, --filter          filter entries not forming putative triplexes (requires: -o, -n, -g)
  -p, --predict         predict putative triplexes
  -t, --test            test stability of predicted triplexes
```

**Example**: Read microrna.org's Human (hg19) [target site predictions](http://www.microrna.org/microrna/getDownloads.do)
in memory, for later filtering for RNA triplex constraints and stability testing:
```
./triplexer -s -o hsa -g hg19 -n microrna_org -i /data/human_predictions_S_C_aug2010.txt
```
<p align="right"><a href="#top">&#x25B2; back to top</a></p>
