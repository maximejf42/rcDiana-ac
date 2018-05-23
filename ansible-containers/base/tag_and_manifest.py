#! python

# Note that for Resin.io compilation, you have to trick the arm compiler into pulling the arm64 image for the raspberry pi3, so add an entry for :armv7hf that is manifested as arch: arm64 variant: v8

# Note that armv7hf is arch: arm, variant: v7, which makes sense but is poorly documented.  Acceptable architectures are listed here:
# https://raw.githubusercontent.com/docker-library/official-images/a7ad3081aa5f51584653073424217e461b72670a/bashbrew/go/vendor/src/github.com/docker-library/go-dockerlibrary/architecture/oci-platform.go

import yaml, logging
from subprocess import call

manifest_file = "rcd-manifests.yml"

def docker_tag(item, new):
    cmd = ['docker', 'tag', item, new]
    logging.debug(cmd)
    call(cmd)

def docker_push(item):
    cmd = ['docker', 'push', item]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_create(prime, aliases):
    cmd = ['docker', 'manifest', 'create', prime, *aliases]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_annotate(prime, item):
    cmd = ['docker', 'manifest', 'annotate',
          prime, item['image'],
          '--arch', item['platform']['architecture'],
          '--os', item['platform']['os'] ]
    if item['platform'].get('variant'):
        cmd = cmd + ['--variant', item['platform']["variant"]]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_push(prime):
    cmd = ['docker', 'manifest', 'push', prime]
    logging.debug(cmd)
    call(cmd)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    with open(manifest_file) as f:
        items = yaml.safe_load(f)

    for item in items:

        prime = item["image"]
        aliases = []

        for m in item["manifests"]:
            docker_tag(m["ac_name"], m["image"])
            docker_push(m["image"])
            aliases.append(m["image"])

        docker_manifest_create(prime, aliases)

        for m in item["manifests"]:
            docker_manifest_annotate(prime, m)

        docker_manifest_push(prime)


