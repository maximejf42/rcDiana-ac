rcDiana AC
==================
Derek Merck <derek_merck@brown.edu>  
Brown University and Rhode Island Hospital  
Spring 2018

Source: <http://github.com/derekmerck/rcdiana-ac>  
Docker Hub: <https://hub.docker.com/u/rcdiana/>

[![Build Status](https://travis-ci.org/derekmerck/rcDiana-ac.svg?branch=master)](https://travis-ci.org/derekmerck/rcDiana-ac)

Overview
---------------

A remotely configured [DIANA][] infrastructure stack, suitable for multi-architecture use with [resin.io][].  Implemented with [ansible-container][].

[DIANA]: https://diana.readthedocs.io
[ansible-container]: https://docs.ansible.com/ansible-container/
[resin.io]: https://www.resin.io


Services
------------------

rcDIANA containers are based on Debian stretch.  They provide multiarchitecture DIANA service containers for amd64 (Intel), armv7hf (Raspberry Pi 3).  _Support for aarch64 (Jetson TX2) is in progress_.

- `dicom`  - vanilla [Orthanc][] - uses ports: 4242 (DICOM), 8042 (http)
- `python` - base [Conda][] Python 2.7 installation
- `learn`  - extends `python` with [TensorFlow][] and [Keras][]
- `movidius` - vanilla Python 3.6 with the [Movidius Neural Compute SDK][]
- `sshd`   - sshd server for remote access

[Orthanc]: http://www.orthanc-server.com
[Conda]: http://www.anaconda.org
[BerryConda]: https://github.com/jjhelmus/berryconda
[TensorFlow]: https://www.tensorflow.org
[Keras]: https://keras.io
[Movidius Neural Compute SDK]: https://github.com/movidius/ncsdk


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

1. Get a conductor image.  Working conductor images can be pulled from the rcdiana namespace on Docker Hub, but need to be retagged as local or ansible-container will not find them (see the `.travis.yml` file).  You can also build your own conductors by cross-compiling a conductor configuration using Resin.io base images.

```bash
$ cd ansible-containers/conductors
$ docker-compose build
```

This provides conductor images tagged to be used with Resin.io's standard [base images](https://docs.resin.io/reference/base-images/resin-base-images/) named `resin-amd64-debian:stretch` and `resin-armv7hf-debian:stretch`.  The armv7hf compilation of crypto, etc. can take a _long_ time.

2.  Build Diana base services from roles.

```bash
$ cd ansible-containers/base
$ ansible-container build
```

3. Push them to your namespace.  Because ansible-container does not have an easily scripted tagging function, the images can be retagged, manifested for multiarchitecture pulls, and pushed to a the correct namespace with another script, `manifest-it.py`.  The manifest format is straight-forward to understand and based on the `manifest.yml` format described at <https://github.com/estesp/manifest-tool>

```bash
$ python manifest-it.py rcd-manifest.yml
```

Update builds are automated with [Travis CI][].  Multi-archicture cross-compiling is done using [qemu-user-static](https://github.com/multiarch/qemu-user-static) embedded in the resin base images.  See this post for details: <https://blog.hypriot.com/post/setup-simple-ci-pipeline-for-arm-images/>

[Travis CI]: https://travis-ci.org

Configuration
------------------

### Conda for armv7hf

Because armv7hf is no longer supported by Continuum as of 2015, rcDiana uses [BerryConda][].

To build the `conda` image with a different Conda distribution, such as Continuum's Python 2.7.10 armv7l release, override the environment variable `CONDA_PKG` to the appropriate download location at build-time.  

The most recent (but quite outdated) Continuum miniconda for armv7hf can be found at: <https://repo.continuum.io/miniconda/Miniconda-3.16.0-Linux-armv7l.sh>

A recent passing build of tensorflow for armv7hf can be found at: <http://ci.tensorflow.org/view/Nightly/job/nightly-pi/lastSuccessfulBuild/>

### Conda for aarch64

Conda can be built from `conda-constructor` for arm64.

```bash
$ mkdir /tmp/pkg
$ docker build -t pkg ./conda_aarch64_pkg
$ docker run -it -v "/tmp/pkg:/host/pkg" pkg
```

In practice, this seems to have a very limited package set (no numpy, etc.)

### h5py

2.7 throws some `__future__` warnings when importing keras.  Supress them by invoking python with

```bash
$ python -W ignore
```


## License

MIT
