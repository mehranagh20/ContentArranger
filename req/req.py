import shutil
import sys
import os
import re


try:
    path = os.path.expanduser('~/Documents')
    if not os.path.exists(path): os.makedirs(path)
    path = os.path.join(path, 'ContentArranger')
    os.makedirs(path)
    shutil.copy('DefaultTypes', path)
    shutil.copy('UserDefinedTypes', path)
    shutil.copy('contentArranger.py', path)
    shutil.copy('help', path)

except:
    print('Problem making folder in', path, '\nmake sure you have permission to create folder there or the folder already exists .')
    sys.exit(1)

linux, mac = 'linux*', 'darwin*'
path = os.path.join(path, 'contentArranger.py')
command = 'alias cArrange=' + '"' + 'python3 '  + path + '"\n'

found = False

if(re.match(linux, sys.platform)):
    try: f = open(os.path.expanduser('~/.bashrc'), 'a')
    except:
        print('problem opening ~/.bashrc file .')
        sys.exit(1)

    found = True

elif(re.match(mac, sys.platform)):
    if not os.path.exists('~/.bash_profile'):
        f = open(os.path.expanduser('~/.bash_profile'), 'w')
    else:
        try: f = open(os.path.expanduser('~/.bash_profile'), 'a')
        except:
            print('problem opening ~/.bash_profile file .')
            sys.exit(1)

    found = True

if found:
    f.write(command)

f.close()

