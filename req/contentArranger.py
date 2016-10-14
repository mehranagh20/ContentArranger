import magic
import re
import pickle
from multiprocessing import Process
import sys
import os
import shutil
import datetime


UserDefinedTypes, DefaultTypes = os.path.expanduser('~/Documents/ContentArranger/UserDefinedTypes'), os.path.expanduser('~/Documents/ContentArranger/DefaultTypes')


class fileOpenError(IOError):
    def __init__(self, fileName):
        super(fileOpenError, self).__init__("Error while opening " + fileName)


class movingFileError(Exception):
    def __init__(self):
        super(movingFileError, self).__init__('Error while moving files')


class doesntExistError(Exception):
    def __init__(self, path):
        super(doesntExistError, self).__init__(path, "doesn't exists .")


def scanFiles(folderName, defaultT=True, commandLine=False):

    '''function scans files in folder and return list of processes to be done...'''

    try:
        f = open(UserDefinedTypes, 'rb')
    except IOError:
        if commandLine:
            print('could not open UserDefinedTypes .')
            sys.exit(1)
        raise fileOpenError('UserDefinedTypes')
    userList = pickle.load(f)
    f.close()

    try:
        f = open(DefaultTypes, 'rb')
    except IOError:
        if commandLine:
            print('could not open DefaultTypes .')
            sys.exit(1)
        raise fileOpenError('DefaultTypes')
    defaultList = pickle.load(f)
    f.close()

    processList = []
    for file in os.listdir(folderName):
        if file[0] == '.':
            continue
        path = os.path.join(folderName, file)
        if not os.path.isfile(path) or os.path.isdir(path): continue
        try:
            type = magic.from_file(path)
        except:
            print('There was a problem reading', file, file=sys.stderr)
            continue
        usrDef = False
        for tup in userList:
            if tup and type in tup[1]:
                usrDef = True
                if tup[0] != '-1':
                    processList.append((path, os.path.join(folderName, tup[0])))
                break

        if not usrDef and defaultT:
            found = False
            for tup in defaultList:
                for exp in tup[1]:
                    if re.match(exp, type):
                        found = True
                        processList.append((path, os.path.join(folderName, tup[0])))
                        break
                if found: break

            if not found:
                processList.append((path, os.path.join(folderName, 'Others')))

    return processList


def arrange(folderName, defaultT=True, flag=False, processNum=10, commandLine=False):

    '''function manages the arrage...'''

    if not os.path.exists(folderName):
        if commandLine:
            print(folderName, 'does not exists .')
            sys.exit(1)
        raise doesntExistError(folderName)
    if not os.path.isdir(folderName):
        if commandLine:
            print(folderName, 'is not a directory .')
            sys.exit(1)
        raise Exception(folderName, 'is not a directory .')

    processList = scanFiles(folderName, defaultT, commandLine)

    if flag:
        try:
            print(datetime.date.today())
            logFile = open(os.path.join(folderName, str(datetime.date.today()) + '.txt'), 'w')
            print(os.path.abspath(folderName), file=logFile)
        except IOError:
            if commandLine:
                print('could not create logfile .')
                sys.exit(1)
            raise Exception('could not create logfile .')

    for pr in processList:
        if not os.path.exists(pr[1]):
            os.makedirs(pr[1])
            if flag: print('making', os.path.basename(pr[1]), file=logFile)

    doing = []
    for i in processList[:processNum]:
        if not os.path.exists(os.path.join(i[1], os.path.basename(i[0]))):
            doing.append(Process(target=shutil.move, args=(i)))
            doing[-1].start()
            if flag: print('moving', os.path.basename(i[0]), 'to', os.path.basename(i[1]),file=logFile)
        else:
            print('problem moving', os.path.basename(i[0]),'. file with this name already exists in', os.path.basename(i[1]), '.', file=sys.stderr)
        i = processNum

    try:
        while doing:
            doing[0].join()
            del doing[0]

            if len(processList) > i:
                if not os.path.exists(os.path.join(processList[i][1], os.path.basename(processList[i][0]))):
                    doing.append(Process(target=shutil.move, args=processList[i]))
                    doing[-1].start()
                    if flag: print('moving', os.path.basename(processList[i][0]), 'to', os.path.basename(processList[i][1]), file=logFile)
                else:
                    print('problem moving', os.path.basename(processList[i][0]),'. file with this name already exists in', os.path.basename(processList[i][1]), '.', file=sys.stderr)
                i += 1
    except:
        raise movingFileError()
    return True


def removeType(sampleFile, folderName, commandLine=False):

    '''function that removes user defined types...'''

    if not os.path.exists(sampleFile):
        if commandLine:
            print('problem reading', sampleFile, '.')
            sys.exit(1)
        raise doesntExistError(sampleFile)

    type = type = magic.from_file(sampleFile)

    try:
        f = open(UserDefinedTypes, 'rb')
    except IOError:
        if commandLine:
            print('could not open UserDefinedTypes .')
            sys.exit(1)
        else:
            raise fileOpenError('UserDefinedTypes')

    list = pickle.load(f)
    f.close()

    found = False
    for i in range(len(list)):
        if list[i] and list[i][0] == folderName:
            found = True
            if not type in list[i][1]:
                if commandLine:
                    print('There is no such type in', folderName, ".")
                    sys.exit(1)
                raise Exception("Type doesn't exits .")
            list[i][1].remove(type)
            break
    if not found:
        if commandLine:
            print(folderName, 'does not exist.')
            sys.exit(1)
        raise Exception(folderName, "doesn't exists .")

    try:
        f = open(UserDefinedTypes, 'wb')
    except IOError:
        raise fileOpenError('UserDefinedTypes')

    pickle._Pickler(f, 2).dump(list)
    f.close()
    if commandLine:
        print(type, 'removed from', folderName, '.')
        sys.exit(0)
    else: return True


def addType(sampleFile, folderName, commandLine=False):

    '''function that let the user define specific types...'''

    if not os.path.exists(sampleFile):
        if commandLine:
            print('problem reading', sampleFile, '.')
            sys.exit(1)
        raise doesntExistError(sampleFile)

    type = magic.from_file(sampleFile)

    try:
        f = open(UserDefinedTypes, 'rb')
    except IOError:
        if commandLine:
            print('could not open', 'UserDefinedTypes', '.')
            sys.exit(1)
        raise fileOpenError('UserDefinedTypes')

    list = pickle.load(f)
    f.close()

    folderInd = -1
    for i in range(len(list)):
        if list[i] and type in list[i][1]:
            if commandLine:
                if folderName != list[i][0]:
                    print('This type already exists in', list[i][0],
                          'folder, first try to remove it with "... --remove SampleFile FolderName" in order to add it to', folderName, file=sys.stderr)
                else: print('This type already exists in this folder.', file=sys.stderr)
                sys.exit(1)
            else:
                raise Exception('Type already exists .')
        if list[i] and list[i][0] == folderName: folderInd = i
    if folderInd != -1: list[i][1].append(type)
    else: list.append((folderName, [type,]))

    try:
        f = open(UserDefinedTypes, 'wb')
    except IOError:
        raise fileOpenError('UserDefinedTypes')

    pickle._Pickler(f, 2).dump(list)
    f.close()

    if commandLine:
        print(type, 'added to', folderName)
        sys.exit(0)
    return True


def reset(commandLine=False):

    '''function that resets the UserDefined file to hold nothing...'''

    if not os.path.exists(UserDefinedTypes):
        if commandLine:
            print('could not open', 'UserDefinedTypes .')
            sys.exit(1)
        raise doesntExistError('UserDefinedTypes')

    try:
        f = open(UserDefinedTypes, 'wb')
    except IOError:
        raise fileOpenError('UserDefinedTypes')

    l = [()]

    pickle._Pickler(f, 2).dump(l)
    f.close()

    if commandLine:
        print('No user defined types anymore .')
        sys.exit(0)
    return True


def recover(logFile, processNum=10, commandLine=False):

    '''function that recovers a folder base on the logfile ...'''

    try:
        f = open(logFile, 'r')
    except:
        if commandLine:
            print('problem reading logfile .')
            sys.exit(1)
        raise fileOpenError(logFile)

    foldersToDelete, filesToMove, list = [], [], [i for i in f.read().split('\n')]
    f.close()

    path = list[0]
    if not os.path.exists(path):
        if commandLine:
            print(path, 'does not exists .')
            sys.exit(1)
        else:
            doesntExistError(path)

    del list[0]
    if not os.path.exists(path):
        if commandLine:
            print('path specified in log file does not exists')
            sys.exit(1)
        raise doesntExistError(path)

    for log in list:
        if not log: continue
        tmpL = log.split()
        if tmpL[0] == 'making':
            if os.path.exists(os.path.join(path, " ".join(tmpL[1:]))):
                foldersToDelete.append(" ".join(tmpL[1:]))
        else:
            if os.path.exists((os.path.join(os.path.join(path, " ".join(tmpL[3:])), tmpL[1]))):
                filesToMove.append((os.path.join(os.path.join(path, " ".join(tmpL[3:])), tmpL[1]), path))

    procs = [Process(target=shutil.move, args=i) for i in filesToMove[:processNum] if (not os.path.exists(os.path.join(path, os.path.basename(i[0]))))]
    i = processNum
    for process in procs: process.start()

    while procs or i < len(filesToMove):
        if procs:
            procs[0].join()
            del [procs[0]]
        if i < len(filesToMove):
            k = filesToMove[i]
            if not os.path.exists(os.path.join(path, os.path.basename(k[0]))) and os.path.exists(k[0]):
                procs.append(Process(target=shutil.move, args=k))
                procs[-1].start()
            i += 1

    for folder in foldersToDelete:
        if len(os.listdir(os.path.join(path, folder))) == 0: os.removedirs(os.path.join(path, folder))

    try: os.remove(logFile)
    except:
        if commandLine:
            print('problem removing logfile .')
            sys.exit(1)
        return False

    if commandLine:
        print(path, 'recovered successfully .')
        sys.exit(0)
    return True


def help(commandLine=False):
    try:
        f = open(os.path.expanduser('~/Documents/ContentArranger/help'), 'r')
        if(commandLine): print(f.read())
        else: return f.read()
    except:
        print('problem opening help file .')



def main():
    del sys.argv[0]
    if len(sys.argv) < 1 or (len(sys.argv) > 3 and (sys.argv[0] != '--add' and sys.argv[0] != '--remove')) or (
                    len(sys.argv) == 2 and (sys.argv[0] != '--log' and sys.argv[0] != '--recover' and sys.argv[0] != '--off')) or (
            len(sys.argv) == 3 and ((sys.argv[0] != '--add' and sys.argv[0] != '--remove') and (sys.argv[0] != '--off' or sys.argv[1] != '--log'))):
        print("Wrong Usage, Type 'command --help' to see available options .")
        sys.exit(0)
    #in case of adding new type
    if sys.argv[0] == '--add': addType(sys.argv[1], " ".join(sys.argv[2:]), True)
    elif sys.argv[0] == '--remove': removeType(sys.argv[1], " ".join(sys.argv[2:]), True)
    elif len(sys.argv) == 1:
        if(sys.argv[0] == '--reset'): reset(True)
        elif(sys.argv[0] == '--help'): help(True)
        else: arrange(sys.argv[0], True, False, 10, True)
    elif len(sys.argv) == 2:
        if sys.argv[0] == '--log': arrange(sys.argv[1], True, True, 10, True)
        elif sys.argv[0] == '--off': arrange(sys.argv[1], False, False, 10, True)
        elif sys.argv[0] == '--recover': recover(sys.argv[1], 10, True)
    elif len(sys.argv) == 3:
        arrange(sys.argv[2], False, True, 10, True)



if __name__ == '__main__': main()

