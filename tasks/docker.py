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
    c.run(f'nohup docker run --network=host --rm -v {current_file_dir}/../build/tmp/deploy/images/iot-edge:/tftpboot --name deploy -t deploy_server:latest')

def run_http(c):
    c.run(f"docker run -dit --name my-apache-app -p 8080:80 -v {current_file_dir}/../build/tmp/deploy/images/iot-edge:/tftpboot:/usr/local/apache2/htdocs/images httpd:2.4")

@task
def clean(c, image="iot-edge-image"):
    c.run('docker stop deploy')