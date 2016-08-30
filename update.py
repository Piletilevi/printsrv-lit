# coding: utf-8

from os import environ, path, chdir, remove
from urllib2 import urlopen, URLError, HTTPError

from json import load as loadJSON
from json import loads as loadsJSON
from json import dumps as dumpsJSON
from sys import argv, stdout

from zipfile import ZipFile

print(argv)

if not 'plp_update_to_version' in environ:
    raise IndexError('Missing "plp_update_to_version" in environment variables.')
UPDATE_TO_TAG = environ['plp_update_to_version']


def dlfile(url):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open(path.basename(url), "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


def version_info():
    with open('package.json', 'rU') as package_file:
        try:
            local_package_json = loadJSON(package_file)
        except ValueError:
            print('WARNING: local package.json is damaged.')
            local_package_json = {'version': 'N/A'}
    return local_package_json['version']


L_VER = version_info()
if L_VER == UPDATE_TO_TAG:
    print('Already at {0} (tag:"{1}")'.format(L_VER, UPDATE_TO_TAG))
    exit(0)


print('Update required: local:"{0}" <= remote: "{1}".'.format(L_VER, UPDATE_TO_TAG))


REMOTE_PLEVI = 'https://github.com/Piletilevi/printsrv/releases/download/{0}/plevi_{0}.zip'.format(UPDATE_TO_TAG)
REMOTE_PRINTSRV = 'https://github.com/Piletilevi/printsrv/releases/download/{0}/printsrv_{0}.zip'.format(UPDATE_TO_TAG)
REMOTE_RASOASM = 'https://github.com/Piletilevi/printsrv/releases/download/{0}/RasoASM_{0}.zip'.format(UPDATE_TO_TAG)


chdir('..')

dlfile(REMOTE_PLEVI)
with ZipFile('plevi_{0}.zip'.format(UPDATE_TO_TAG), "r") as z:
    z.extractall()
remove('plevi_{0}.zip'.format(UPDATE_TO_TAG))

dlfile(REMOTE_PRINTSRV)
with ZipFile('printsrv_{0}.zip'.format(UPDATE_TO_TAG), "r") as z:
    z.extractall('.\\printsrv')
remove('printsrv_{0}.zip'.format(UPDATE_TO_TAG))

dlfile(REMOTE_RASOASM)
with ZipFile('RasoASM_{0}.zip'.format(UPDATE_TO_TAG), "r") as z:
    z.extractall('.\\RasoASM')
remove('RasoASM_{0}.zip'.format(UPDATE_TO_TAG))

print('printsrv update finished.')
