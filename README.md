<div id="top"></div>



# Triplexer

The Triplexer is a computational pipeline that builds the backend database of
the [TriplexRNA](https://triplexrna.org).

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

To use the Triplexer, you first need to build and run its Docker container:
```
docker build -t triplexer .
docker run -it -v $(pwd):/tmp triplexer:latest
```

Once inside the container's interactive environment, the Triplexer can be
launched from the command line.  
The full list of options is revealed by running the Triplexer without
arguments:

```
$ ./triplexer

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print the version and exit
  -i CONF, --init CONF  set CONF as the init configuration file (default:
                        conf.yaml)
  -x CORES, --exe CORES
                        set CORES as the number of parallel execution cores
                        (default: 2)
  -l STORE, --location STORE
                        set STORE as the location for all intermediate results
                        (default: 127.0.0.1:6379)
  -d DB, --db DB        set DB as the location database for all intermediate
                        results (default: 0)

target organism data:
  -o ORG, --org ORG     set ORG as the target organism
  -n NS, --ns NS        set NS as the target organism's namespace
  -g GEN, --genome GEN  set GEN as the target organism's genome release
  -f FILE, --file FILE  set FILE as the target organism's source dataset file

operations:
  -c, --cache           cache the provided source dataset (requires options
                        -o, -n, -g, -f)
  -a, --allowed         discard all cached entries that do not form any
                        putative triplex (requires options -o, -n, -g)
  -p, --predict         predict putative triplexes
  -s, --simulate        simulate the stability of predicted putative triplexes
```

<p align="right"><a href="#top">&#x25B2; back to top</a></p>
