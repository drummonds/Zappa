import os
from pathlib import Path
import sys

# add the Lambda root path into the sys.path
sys.path.append('/var/task')
import subprocess

# ------------- Start if fix to try and get project to work
# add the hellodjango project path into the sys.path
# sys.path.append('<PATH_TO_MY_DJANGO_PROJECT>/hellodjango')
#
# # add the virtualenv site-packages path to the sys.path
# sys.path.append('<PATH_TO_VIRTUALENV>/Lib/site-packages')
#
# # poiting to the project settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellodjango.settings")
# ------------- end of fix

def h3_list_dir(this_dir):
    cmd = ['ls', f'{this_dir }','-als']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    print(' =>'.join((f'Dir {this_dir}: ' + o.decode('ascii')).split('\n'))[:4096])
    # print('Error: ' + e.decode('ascii'))
    # print('code: ' + str(proc.returncode))

def h3_list_env(search_key = 'DJANGO'):
    cmd = ['env',]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    r = ' || '.join([i for i in ('env Output: ' + o.decode('ascii')).split('\n') if i[:len(search_key)] == search_key])
    if r:
        print(r)
    else:
        print(f'No environment variables starting with {search_key} found')


def get_django_wsgi(settings_module):
    print(f"H3 about to start with path {sys.path}, python version {sys.version_info}")
    print(f'Scan /tmp/bytestone for files CWD = {os.getcwd()}')
    h3_list_dir('/tmp')
    h3_list_dir('/var')  # Test if odd recursive search happens
    h3_list_env()
    results = []
    for entry in os.scandir('/tmp/bytestone'):
        p = Path(entry.path)
        if p.parent == Path('/tmp/bytestone'):
            if entry.is_file():
                results.append(f'file: {entry.name}')
            else:
                results.append(f'dir: {entry.name}')

    h3_list_dir('/tmp/bytestone')
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    import django

    if django.VERSION[0] <= 1 and django.VERSION[1] < 7:
        # call django.setup only for django <1.7.0
        # (because setup already in get_wsgi_application since that)
        # https://github.com/django/django/commit/80d74097b4bd7186ad99b6d41d0ed90347a39b21
        django.setup()

    return get_wsgi_application()
