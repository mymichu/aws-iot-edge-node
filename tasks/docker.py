from invoke import task
import pathlib
import shutil

import os
import io


current_file_dir = pathlib.Path(__file__).parent.absolute()

@task
def setup(c):
    c.run(f"docker build {current_file_dir}/../docker -t deploy_server:latest")
    
@task
def run(c, image="iot-edge-image"):
    c.run(f'nohup docker run --rm --network=host --rm -v {current_file_dir}/../build/tmp/deploy/images/iot-edge:/tftpboot --name deploy -t deploy_server:latest')

@task
def clean(c, image="iot-edge-image"):
    c.run('docker stop deploy')