# Imports
import pathlib
import requests
from urllib.request import urlopen
import json
import re
import os
import subprocess
import shutil
import jinja2

# Setup
initial_path = str(pathlib.Path(__file__).parent.absolute())

# Compile reusable regular expressions
semantic_versioning = re.compile(r'^v?[0-9]+\.[0-9].*$')
semantic_versioning_with_v = re.compile(r'^v[0-9]+\.[0-9].*$')

# Check repos in repositorries.txt for new releases
repos = open('repositories.txt', 'r').read().split('\n')[:-1]
for repo in repos:
    repo_api_url = 'https://api.github.com/repos/{}/releases'.format(repo)
    repo_name = repo.split(r'/')[-1]
    if requests.get(repo_api_url).status_code != 200:
        print('Repository "{}" could not be found.'.format(repo))
    else:
        releases = json.loads(urlopen(repo_api_url).read().decode('utf-8'))
        for release in releases:
            version = release['tag_name']
            if semantic_versioning_with_v.match(version):
                version_no_v = version[1:]
            else:
                version_no_v = version
            version_dir = '/'.join([repo_name, version_no_v])

            # If a new release is found:
            if not os.path.isdir(version_dir):

                # Make directory for that version
                print('New release found: "{}" version "{}"'.format(repo_name, version))
                if not semantic_versioning.match(version):
                    print('Warning: Release version "{}" does not comply with semantic versioning conventions.'.format(version))
                os.mkdir(version_dir)
                os.chdir(version_dir)

                # Download repository and switch to appropriate release
                subprocess.run('git clone git@github.com:{}.git'.format(repo), shell=True)
                os.chdir(repo_name)
                subprocess.run('git checkout tags/{} -b {}-branch'.format(version, version), shell=True)

                # Build module
                subprocess.run('sh ../../compile_instructions.sh', shell=True)

                # Create directories for lua files if they don't already exist
                os.chdir(initial_path)
                os.chdir(repo_name)
                if not os.path.isdir('modules'):
                    os.mkdir('modules')
                os.chdir('modules')
                if not os.path.isdir('Core'):
                    os.mkdir('Core')
                os.chdir('Core')
                if not os.path.isdir(repo_name):
                    os.mkdir(repo_name)
                os.chdir(repo_name)

                # Create lua file
                loader = jinja2.PackageLoader(__name__, '/'.join([initial_path, repo_name]))
                env = jinja2.Environment(
                    loader=loader,
                )
                template = env.get_template('template.lua')
                populated = template.render(
                    version = version_no_v,
                    root_path = '/'.join([initial_path, version_dir, repo_name]),
                )
                open('{}.lua'.format(version_no_v), 'w').write(populated)
                os.chdir(initial_path)

# to-do
# test on sparc, psi4, and a cmake program kevin will find
# allow the module name to be something different from the repo name?
# make sure they dont name a version "module" (and possibly enforce semantic versioning conventions)
# think of way to avoid multiple people adding a module of the same name (e.g. separate by username)
# add documentation/instructions
# polish- make impossible to break, easy to use, and easy to debug. Print if any needed files are missing
# logging (possibly change all my print statements) (silence git clone and other noisy commands?)
# support gitlab repos
# security concenrns: limit number of versions, number of files per repo and total storage allocated to each module.ALSO, MAKE SURE THAT THE BASH SCRIPT THEY PROVIDE IS NOT RUN WITH SUPERUSER AUTHORITY AND CAN'T, SAY, REMOVE OTHER PEOPLES' MODULES OR MESS UP ANYTHING ELSE
