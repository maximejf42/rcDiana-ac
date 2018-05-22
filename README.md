rcDiana AC
===================

Derek Merck <derek_merck@brown.edu>
Spring 2018

A multi-architure Diana service stack implementation using [ansible-container][] and suitable for remote configuration va  [resin.io][].

[ansible-container]: https://docs.ansible.com/ansible-container/
[resin.io]: https://www.resin.io

Usage
-------------------

1. Build cross-compiling conductors from Resin.io base images.

```bash
$ cd ansible-containers/conductors
$ docker-compose build
```

This provides conductor images tagged to be used with [base images](https://docs.resin.io/reference/base-images/resin-base-images/) `resin-amd64-debian:stretch` and `resin-armv7hf-debian:stretch`.  The armv7hf compilation of crypto, etc. can take a LOG time.

# TODO: SHOULD PUSH THEM TO CONDUCTOR REPOS, SO WE CAN PULL AND RETAG ON TRAVIS

Kill all running docker containers if needed.

```bash
$ docker stop $(docker ps -aq)
```

Build Diana base services from roles.
```bash
$ cd ansible-containers/base
$ ansible-container build
```

Push containers to Docker Hub namespace, resin.io projects, or other registries.  `tag_and_push.sh` creates a multi-architecture repo.

```bash
$ sh tag_and_push.sh
```

Push the update to resin.io, which will rebuild the images in the root docker-compoose.yml



Architecture names for multiarch:

https://raw.githubusercontent.com/docker-library/official-images/a7ad3081aa5f51584653073424217e461b72670a/bashbrew/go/vendor/src/github.com/docker-library/go-dockerlibrary/architecture/oci-platform.go