from invoke import task
import pathlib
import shutil

import os
import io


current_file_dir = pathlib.Path(__file__).parent.absolute()

@task
def clean(c, buildfolder='build'):
    buildfolder=f"{current_file_dir}/../{buildfolder}"
    if not os.path.isdir(buildfolder):
        c.run(f"rm -rf {buildfolder}")

@task
def setup(c, buildfolder='build'):
    out = c.run(f"TEMPLATECONF={current_file_dir}/../layers/meta-iot-edge/conf source {current_file_dir}/../layers/poky/oe-init-build-env {current_file_dir}/../{buildfolder} && env", hide="stdout")
    buf=io.StringIO(out.stdout)
    f = open(f"{current_file_dir}/../{buildfolder}/setup-env", "w")
    f.write("#!/usr/env bash\n")
    for line in buf:
        (key, _, value) = str(line).partition('=')
        if key and value != "":
            os.environ[key] = value
            f.write(f'export {key}="{str(value).rstrip()}"\n')
    f.close()
    
@task
def build(c, image="iot-edge-image"):
    c.run(f'bash -c "source {current_file_dir}/../build/setup-env && bitbake {image}"')
