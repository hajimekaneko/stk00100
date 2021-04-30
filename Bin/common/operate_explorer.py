import subprocess

def common_openFile(vlsOpenFileName):
    subprocess.run('explorer "{}"'.format(vlsOpenFileName).replace("/", "\\"))