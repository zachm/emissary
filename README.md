# emissary

emissary is a proxy service for third party email apps. It accepts data via a HTTP POST `/email` endpoint,
validates that data in several ways, and then passes it on to one of its supported SaaS email providers.
Which of these providers is used - or in which ratio they are used together - can be controlled via a
config file in the root of the service.


## Design

emissary is a RESTful web application built with Python 3, uWSGI, and Flask. It runs in a Docker
container configured with Ubuntu Xenial LTS.

Flask is a strong go-to web framework: it's reasonably lightweight and very simple in its default
configuration. uWSGI will handle a multi-process web server at thousands of QPS on a single instance;
it's also easy to configure. emissary is set up conservatively; feel free to tweak the uWSGI
configuration in `emissary.uwsgi.ini` to suit your needs.

By packaging emissary in Docker; you can run it almost anywhere. Though the app runs on Ubuntu, it was
solely developed on OS X. Docker gives inordinate amounts of flexibility; what little overhead it
creates can be overcome by a simple `Makefile` like the one I've included.

To scale emissary, simply launch more containers. Use a load balancer of your choice in front of them.

Within Python, emissary follows a reasonably modular OO code layout. For example, adding an additional
email provider involves changing a config file and writing ~40 lines of code to munge emissary's data
into whichever sort of payload the provider requires.


## Configuration
These directions assume you have a computer with Docker already installed.

First, in emissary's base directory, copy the file `emissary.yaml.example` to `emissary.yaml`.

Next, edit the file you just created. Replace the fake credentials for each provider (Mailgun and
Mandrill) with valid ones. Note that Mailgun's URL format requires your domain name to be included
midway through its endpoint.

emissary allows you to control the amount of traffic you send to each email provider via the
configuration fields called `enabled`. This field is a float from 0.0 to 1.0, ranging from no
traffic to all traffic. It is important that the sum of all `enabled` fields is 1.0.


## Running, Developing, and Debugging
Due to emissary's use of Docker, these operations are all very similar. emissary listens on port `8080`
by default; this is enforced via Docker's port mapping feature.

`make run`: Starts a productionized, multi-process copy. This will build a Docker container, install all
dependencies, and spawn a uWSGI server within it. To exit, your favorite keyboard interrupt works; you
can also use the Docker CLI.

`make debug`: A single-threaded server, it auto reloads on every code change. For development only.

`make interactive`: Drops into a shell within a new Docker container. Useful for debugging packages and
build dependencies.

`make test`: Run the unit tests included with emissary.

`make coverage`: Generate a lines of code coverage report. As of press time, emissary had 91% coverage.



## Future Work
__Logging Subsystem.__ There's a rudimentary logging config in `emissary/__init__.py`, but this could
be improved on. Depending on a choice of PaaS, care must be taken to pipe logs to the right place for
analysis.

__Real-time Monitoring.__ This system cries out for a time series dashboard. Integrating one of the
many statsd client libraries would be a good place to start. From there, it's pretty straightforward to
set up alerting (even with a SaaS provider) to notify on-call personnel when the service - or its
downstream partners - return an inordinate amount of failure cases.

__Circuit Breaking.__ Circuit breaking is a concept where, if a downstream provider begins returning
failed responses (especially 500-class errors) the owning system will stop sending it traffic. If
applied across an entire service topology, this creates an effective form of backpressure in addition
to what TCP provides. If the circuit breaker's source of truth exists across the entire
deployment environmenrt, the effect will be even more immediate and pronounced.

__Hot Reloading.__ If emissary's configuration is expected to change with any frequency, adding
hot reloads to the config file parsing will enable weights and providers to change without redeploying
the entire service.

__Retries and Rate Limiting.__ As of now, emissary does not retry on its own when an upstream provider
returns a failed response. Similarly, rate limiting has not been implemented.

__Swagger.__ I'd like to get a more thorough service interface available; at present, I've hand-rolled
something similar in spirit to what Swagger does for validation.

__Code Style.__ I'm a recovering Python 2.7 developer, so I'd like to take more advantage of the
latest and the greatest in the Python 3 environment.
