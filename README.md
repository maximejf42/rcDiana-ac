rcDiana AC
==================
Derek Merck <derek_merck@brown.edu>  
Brown University and Rhode Island Hospital  
Spring 2018

Source: <http://github.com/derekmerck/rcdiana-ac>  
Docker Hub: <https://hub.docker.com/u/rcdiana/>


Overview
---------------

A remotely configured [DIANA][] service stack, suitable for multi-architecture use with [resin.io][].  Implemented with [ansible-container][].

[DIANA]: https://diana.readthedocs.io
[ansible-container]: https://docs.ansible.com/ansible-container/
[resin.io]: https://www.resin.io


Services
------------------

rcDIANA is based on Debian stretch, and provides multiarchitecture docker service containers for amd64 (Intel), armv7hf (Raspberry Pi 3).  _Support for aarch64 (Jetson TX2) is in progress_.

- dicom  - vanilla [Orthanc][] - uses ports: 4242 (DICOM), 8042 (http)
- python - base [Conda][] Python 2.7 installation
- learn  - extends python with [TensorFlow][] and [Keras][] _amd64 only for now_
- sshd   - sshd server for remote access

Because armv7hf is no longer supported by Continuum as of 2015, rcDiana uses [BerryConda][].

http://ci.tensorflow.org/view/Nightly/job/nightly-pi/lastSuccessfulBuild/

[Orthanc]: http://www.orthanc-server.com
[Conda]: http://www.anaconda.org
[BerryConda]: https://github.com/jjhelmus/berryconda
[TensorFlow]: https://www.tensorflow.org
[Keras]: https://keras.io


Usage
-------------------

```bash
$ git clone https://www.github.com/derekmerck/rcdiana-ac
$ cd rcDiana
$ docker-compose up
```
Or 

```bash
$ docker run rcdiana/dicom -p "80:8040"
$ docker run -it rcdiana/learn /bin/bash 
```

Or push the repo to an Intel or [Raspberry Pi 3][] Resin.io repository for automated rollout using `docker-compose`.

[Raspberry Pi 3]: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

Building
--------------------

1. Build cross-compiling `ansible-container` conductor images from Resin.io base images.

```bash
$ cd ansible-containers/conductors
$ docker-compose build
```

This provides conductor images tagged to be used with Resin.io's standard [base images](https://docs.resin.io/reference/base-images/resin-base-images/) named `resin-amd64-debian:stretch` and `resin-armv7hf-debian:stretch`.  The armv7hf compilation of crypto, etc. can take a _long_ time.

Working conductor images can also be pulled from the rcdiana namespace on Docker Hub, but need to be retagged as local or ansible-container will not find them.

Build Diana base services from roles.
```bash
$ cd ansible-containers/base
$ ansible-container --config-file base_container.yml build
```

`ansible-container` does not have an easily scripted tagging function, so the images all need to be retagged appropriately, manifested for multiarchitecture pulls, and pushed to a thge correct namespace with another script.

```bash
$ python tag_and_manifest.py rcdiana rcd-manifest.yml
```

Update builds are automated with [Travis CI][].  Multi-archicture cross-compiling is done using [qemu-user-static](https://github.com/multiarch/qemu-user-static) embedded in the resin base images.  See this post for details: <https://blog.hypriot.com/post/setup-simple-ci-pipeline-for-arm-images/>

[Travis CI]: https://travis-ci.org

Configuration
------------------

Broken during refactoring:

The base images respect 3 built-in environment variables:

- `ORTHANC_TITLE` (default: Orthanc-$RCD_ARCH)
- `ORTHANC_PASSWORD` (default: 0rthanC!)
- `ROOT_PASSWORD` (default: passw0rd!)

### Conda for armv7hf

To build the `conda` image with a different Conda distribution, such as Continuum's Python 2.7.10 armv7l release, override the environment variable `CONDA_PKG` to the appropriate download location at build-time.  

The most recent (outdated) Continuum miniconda for armv7hf can be found at <https://repo.continuum.io/miniconda/Miniconda-3.16.0-Linux-armv7l.sh>

### Compiling Conda for aarch64

Conda can be built from `conda-constructor` for arm64 (as contributed by the same person who manages the BerryConda distrubiton).

```bash
$ mkdir /tmp/pkg
$ docker build -t pkg ./conda_aarch64_pkg
$ docker run -it -v "/tmp/pkg:/host/pkg" pkg
```

In practice, this seems to have a very limited package set (no numpy, etc.)

Notes
-----------------

Kill all running docker containers if needed:

```bash
$ docker stop $(docker ps -aq)
```

## License

MIT
