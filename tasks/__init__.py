# !/usr/bin/env python

from invoke import Collection

from tasks import docker, yocto


ns = Collection.from_module(yocto)
ns.add_collection(Collection.from_module(docker, name="deploy"))
