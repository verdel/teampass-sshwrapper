============================================================================
Teampass-sshwrapper - SSH wrapper with teampass password manager integration
============================================================================


What is this?
*************
It is a simple command line wrapper for ssh command with Teampass (https://teampass.net) password manager integration.
``teampass-sshwrapper`` provides an executable called ``tpssh``

**IMPORTANT**: To use the teampass-sshwrapper, you need to modify the file ``api/functions.php`` on the server there Teampass was installed. The modified version of the file ``api/functions.php`` is located in the lib folder in this repository.
This moodified version of functions.php is tested with Teampass 2.1.27.35 and 2.1.27.36.
Also sshpass utility required

Current version of functions.php is synchronized with the upstream version in Teampass repository.

As for the changes in the functions.php that have been made:

**API methods have been added to the function restGet():**

1. For CLI **list** sub-command:

- /list/folders

- /list/items

2. Get item and folder by ID:

- /get/item/{item_id}

- /get/folder/{folder_id}

3. Search item and folder by Title:

- /find/items/{item_title}

- /find/items/{folder_title}


Installation
************
*on most UNIX-like systems, you'll probably need to run the following
`install` commands as root or by using sudo*

**from source**

::

  pip install git+http://github.com/verdel/teampass-sshwrapper

**or**

::

  git clone git://github.com/verdel/teampass-sshwrapper.git
  cd teampass-sshwrapper
  python setup.py install

as a result, the ``tpssh`` executable will be installed into a system ``bin``
directory


Usage
-----
::


  usage: -c [-h] [-s SERVER] [-t TOKEN] host [params [params ...]]

  ssh wrapper with teampass password manager integration

  positional arguments:
    host                  destination host. you can use the format username@host
    params                additional parameters for ssh command
  
  optional arguments:
    -h, --help            show this help message and exit
    -s SERVER, --server SERVER
                          teampass api endpoint. environment variable
                          TPSSH_ENDPOINT can be used
    -t TOKEN, --token TOKEN
                          teampass api token. environment variable TPSSH_KEY can
                          be used