# MetRubert webservice

*(Licensed under the GNU Public License v3)*

This is a webservice for [MetRubert](https://github.com/joostgrunwald/MetRuBert),
a prediction model for metaphors in Dutch and English.
webservice is powered by [CLAM](https://proycon.github.io/clam). It offers a RESTful API as well as a web-interface for human end-users.

## Installation

### Development

Clone this repository, create a virtual environment and install the webservice as follows:

```
$ python3 -m venv env
$ . env/bin/activate
$ ./startserver_development.sh
```

Navigate to ``http://localhost:8080``.

Note that for this to work, Alpino must already be installed on your system (and in your `$PATH` with `$ALPINO_HOME`
also set).

### Production

A ``Dockerfile`` is provided for deployment in production environments.

From the repository root, build as follows:

``
$ docker build -t joostgrunwald/metaphorclam .
``

Consult the [Dockerfile](Dockerfile) for various build-time parameters that you may want to set for your own production environment.

When running, mount the path where you want the user data stored into the container, a directory `metaphorclam-userdata` will be created here:

``
$ docker run -p 8080:80 -v /path/to/data/dir:/data joostgrunwald/metaphorclam
``
