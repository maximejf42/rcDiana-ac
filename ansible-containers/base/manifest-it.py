#! python

# Note that armv7hf is arch: arm, variant: v7, which makes sense but is poorly documented.  Acceptable architectures are listed here:
# https://raw.githubusercontent.com/docker-library/official-images/a7ad3081aa5f51584653073424217e461b72670a/bashbrew/go/vendor/src/github.com/docker-library/go-dockerlibrary/architecture/oci-platform.go

import yaml, logging
from subprocess import call
from argparse import ArgumentParser
import os

def docker_tag(item, new):
    cmd = ['docker', 'tag', item, new]
    if opts.mock:
        cmd = cmd[:1] + ["--config", "."] + cmd[1:]
    logging.debug(cmd)
    call(cmd)

def docker_push(item):
    cmd = ['docker', 'push', item]
    if opts.mock:
        cmd = cmd[:1] + ["--config", "."] + cmd[1:]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_create(prime, aliases):
    cmd = ['docker', 'manifest', 'create', prime, *aliases]
    if opts.mock:
        cmd = cmd[:1] + ["--config", "."] + cmd[1:]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_annotate(prime, item):
    cmd = ['docker', 'manifest', 'annotate',
          prime, item['image'],
          '--arch', item['platform']['architecture'],
          '--os', item['platform']['os'] ]
    if opts.mock:
        cmd = cmd[:1] + ["--config", "."] + cmd[1:]
    if item['platform'].get('variant'):
        cmd = cmd + ['--variant', item['platform']["variant"]]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_push(prime):
    cmd = ['docker', 'manifest', 'push', prime]
    if opts.mock:
        cmd = cmd[:1] + ["--config", "."] + cmd[1:]
    logging.debug(cmd)
    call(cmd)

def parse_args():

    p = ArgumentParser("manifest-it.py can retag, manifest for multiple architectures, and push docker images produced by ansible container")
    p.add_argument("manifest_file", help="File with manifest data and aliases")
    p.add_argument('-d', '--dryrun', action="store_true", help="Retag and manifest but don't push")
    p.add_argument('-m', "--mock", action="store_true", help="Invoke docker with a mocked experimental mode configuration.")

    opts = p.parse_args()
    return opts

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    opts = parse_args()

    with open(opts.manifest_file) as f:
        items = yaml.safe_load(f)

    if opts.mock:
        with open('json.config', 'w') as f:
            f.write('{"experimental":"enabled"}')

    for item in items:

        prime = item["image"]
        aliases = []

        for m in item["manifests"]:
            docker_tag(m["ac_name"], m["image"])
            if not opts.dryrun:
                docker_push(m["image"])
            aliases.append(m["image"])

        docker_manifest_create(prime, aliases)

        for m in item["manifests"]:
            docker_manifest_annotate(prime, m)

        if not opts.dryrun:
            docker_manifest_push(prime)

    if opts.mock:
        os.remove('json.config')
