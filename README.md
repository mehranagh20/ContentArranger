# ContentArranger

`ContentArranger` is a python module that arranges and organizes a folder contents.
this can even be used as a linux and mac command in Terminal.

`ContentArranger` offers plenty of options that can manage arranging folders properly.

this module uses some defined types to arrange folders, you can avoid using it, you can
add your own types and their associated folders for arranging. all explained in `Usage`.

Designed in summer of 2016


## Dependencies

* `python-magic` library:
  
  for imformation about installing python-magic see:
    https://github.com/ahupp/python-magic/blob/master/README.md


## Installation

after installing Dependencies (python-magic)

```bash
$ git clone https://github.com/mehranagh20/ContentArranger
$ cd ContentArranger
$ python3 setup.py install
```

in order to use commands in `linux` and `mac`:

```bash
$ cd ContentArranger/req
$ python3 req.py
```


## Features

* in simplest case `ContentArranger` will arrage a folder with default defined types for it.

* you can avoid using default types, to do that you need too add your own types and their folders.

* it is possible to use default types and your own types at the same time

* you can define a type for `ContentArranger` so it will avoid arranging this kind of files.

* you can add types for arranging with giving a samplefile of that type and foldername to
  `ContentArranger` so this will move that specified type to foldername.

* your defiened types have the first priority for arranging, this means that if a file is
  defined in default types and you define it to go to another folder then it will go to
  your defiened folder.

* you can reset your defined types so it will contain nothing.

* `ContentArranger` can produce a logfile of that contains everything that has been done to a folder.

* you can recover a folder using the same logfile produced while arranging it. so the folder
  will be same as before :).

* `ContentArranger` uses multiprocessing technique in order to speed up arranging.
  by default it processes 10 files a time, you can change it if you use it as module.

* everything has been designed to have flexibility, so you can change almost every option you want.

* `ContentArranger` as Terminal usage will print proper Error messages in case of any error and problem.
  and will raise proper exceptions when you use it as a module makes it easy to debug.

* `ContentArranger` have a help option for terminal use, so you can see every options.

#### It may seems complicated, but start using it and you'll see that it is very handy and easy to use :)


## Usage

#### as module:

* Functions:

```
- arrange(folderName, defaultT=True, flag=False, processNum=10, commandLine=False)
```

  arranges the folder name.

  will return True if the whole operation is successful.
  see implementation for details about exceptions.

  * `Arguments`:

  1. folderName: absolute path of foler you want to arrange.

  2. defaultT: set False if you want to avoid arranging base on default tyeps.
  
  3. flag: set True if you want to create logfile for operation.

  4. processNum: number of files to be processed at a time, by default is 10.

  5. commandLine: should allways be False when you are using it as module.


```
- removeType(sampleFile, folderName, commandLine=False)
```

  removes the type specified by sampleFile in folderName if it is already defiend.

  will return True if removing the specified type is successful.
  see implementation for details about exceptions.

  * `Arguments`:

  1. sampleFile: a file to represent the type you have defined for arranging.

  2. folderName: the folder that type specified by sampleFile is in.

  3. commandLine: should allways be False when you are using it as module.
	

```
- addType(sampleFile, folderName, commandLine=False)
```

  adds the type specified by sample file in folderName if it is not defined in another folder.

  will return True if adding type specified by sampleFile to folderName is successful.
  see implementation for details about exceptions.

  * `Arguments`:

  1. sampleFile: a file to represent the type you want to define for arranging.

  2. folderName: the folder that type specified by sampleFile is in.

  3. commandLine: should allways be False when you are using it as module.


- `reset(commandLine=False):`

  removes all the specified types. leaves the UserDefinedTypes file empty.

  will return True if reseting UserDefiendedTypes is successfull.

  * `Arguments`:

  1. commandLine: should allways be False when you are using it as module.


```
- recover(logFile, processNum=10, commandLine=False)
```

  will recover a folder already arranged with `ContentArranger` with created logfile.

  returns True in case of Success.

  * `Arguments`:

  1. logFile: file created with `ContentArranger` when arranging folder.

  2. processNum: number of files to be processed at a time, by default is 10.

  3. commandLine: should allways be False when you are using it as module.


```
- help(commandLine=False)
```

  returns the whole help file as string.

  * `Arguments`:

  1. commandLine: should allways be False when you are using it as module.


#### as Command in linux or mac:

  after installing `ContetnArranger` you can use cArrage command in terminal
  and using every option.

  to see available options and format see help file or simply type :
  `cArrage --help` in terminal.

  Examples:
```bash

  $ cArrange --help
    (will show list of available options)	

  $ cArrange .
    (will arrange the folder you are in now with default types.)

  $ cArrange --log /home/$USER
    (will arrange /home/$USER folder and create logfile for it. logfile name is day's date)

  $ cArrange --recover /home/$USER/2016-08-12.txt
    (will recover /home/$USER and will be back to before previous command.)

  $ cArrange --log --off /home/$USER
    (will arrange /home/$USER create logfile and will avoid using default types for arranging
       just arrangig base on defined types by user)

  $ cArrange --add /home/sampleFile MyFiles
    (will add type file of sampleFile to MyFiles folder from now on).
  
  *  NOTE: You may think some files have a same type but they do not.
     it is not ContentArranger issue, it is just how file types are.

  $ cArrange --remove /homesampleFile MyFolder
    (will do nothing (error will occur) since sampleFile type was in MyFiles folder not MyFolder.
      if you don't remember which folder you added a file, try to add it to a folder and error message
       will tell you which folder that type belongs to.
```


## Author

My name is Mehran Aghabozorgi, i am a bachelor software engineering student in Isfahan University Of Technology
feel free to send me any comment about this project or any other.

email address: `mehranagh200@gmail.com`


## Licence

This project is licensed under the MIT License. see licence file for more details.















