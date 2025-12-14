# Cli-wrapper 
## A small project to automate CLI based tasks

>_Because we think CLI is here to stay, at least for troubleshooting purposes_  
>_Because we use it on a daily basis_  
>_Because we were tired of reinventing the wheel..._  

We decided to build this small project using Python [pexpect](https://pexpect.readthedocs.org/en/stable/), [argparse](https://docs.python.org/3/library/argparse.html) and [pycrypto](https://www.dlitz.net/software/pycrypto/) modules. 

## What does cli-wrapper do ? 
### It automates login and let you interact with a remote device
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password -r csr1000v-1  -x telnet

csr1000v-1>
csr1000v-1>q
Connection closed by foreign host.

<<< gracefully exited from: csr1000v-1

user@m32e:~/cli-wrapper$
```

### You can switch to Cisco enable mode if you provide a second password
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password enablepassword -r csr1000v-1  -x telnet

csr1000v-1#
csr1000v-1#q
Connection closed by foreign host.

<<< gracefully exited from: csr1000v-1

user@m32e:~/cli-wrapper$
```

### Execute one or several commands on a remote device
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password -r csr1000v-1 -x telnet -c 'sho ip int brief | inc Gi'

terminal length 0
csr1000v-1>	>>> now executing commands from ['sho ip int brief | inc Gi'] on csr1000v-1
sho ip int brief | inc Gi
GigabitEthernet1       10.255.1.90     YES TFTP   up                    up
GigabitEthernet2       10.0.0.62       YES TFTP   up                    up
GigabitEthernet3       10.0.0.50       YES TFTP   up                    up
GigabitEthernet4       10.0.0.2        YES TFTP   up                    up
GigabitEthernet5       10.0.0.6        YES TFTP   up                    up
csr1000v-1>
<<< gracefully exited from: csr1000v-1
```

### Send commands output to a log file
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password -r csr1000v-1 -x telnet -c 'sho ip int brief | inc Gi'
  'show ip route' -l
	>>> now logging output from csr1000v-1 in logs/csr1000v-1_D30A74ADA26C.log
	>>> now executing commands from ['sho ip int brief | inc Gi', 'show ip route'] on csr1000v-1
<<< gracefully exited from: csr1000v-1
```

You cannot mix --logfile and --interact when you launch a new session. 
However, once an interactive session is established, and you want to capture a specific output, 
you just hit the escape character (^$ by default) and then you are prompted as follows: 

```
RP/0/RP0/CPU0:demo-edge-4#
RP/0/RP0/CPU0:demo-edge-4#(cli-wrapper) [l]og on/off, [q]uit, [c]ontinue ? l
>>> logging started for host 172.31.2.4 in logs/172.31.2.4_20251209200808.txt

RP/0/RP0/CPU0:demo-edge-4#sho version
Tue Dec  9 19:08:00.073 UTC
Cisco IOS XR Software, Version 24.2.2
Copyright (c) 2013-2024 by Cisco Systems, Inc.
```

Once you are done with logging, just hit the escape character once again: 
```
RP/0/RP0/CPU0:demo-edge-4#sho platform
Tue Dec  9 19:08:03.734 UTC
Node              Type                       State             Config state
--------------------------------------------------------------------------------
0/0/CPU0          R-IOSXRV9000-LC-C          IOS XR RUN        NSHUT
0/RP0/CPU0        R-IOSXRV9000-RP-C(Active)  IOS XR RUN        NSHUT
RP/0/RP0/CPU0:demo-edge-4#(cli-wrapper) [l]og on/off, [q]uit, [c]ontinue ? l
>>> logging is now OFF for host 172.31.2.4

RP/0/RP0/CPU0:demo-edge-4#
```

### Send a batch of commands from a file
```
user@m32e:~/cli-wrapper$ cat > commands/sample_2
show ip route
show ip int brief
sho logging
user@m32e:~/cli-wrapper$
user@m32e:~/cli-wrapper$ cli.py -u username -w password -r csr1000v-1 -x telnet -cf commands/sample_2 -l
	>>> now logging output from csr1000v-1 in logs/csr1000v-1_7C4C722E185B.log
	>>> now executing commands from ['show ip route', 'show ip int brief', 'sho logging'] on csr1000v-1
<<< gracefully exited from: csr1000v-1
```

### Send a batch of commands to a list of hosts
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password -f hosts/liste_csr1000v -x telnet -cf commands/sample_2 -l
	>>> now logging output from csr1000v-1 in logs/csr1000v-1_F69181CBB187.log
	>>> now executing commands from ['show ip route', 'show ip int brief', 'sho logging'] on csr1000v-1
<<< gracefully exited from: csr1000v-1
	>>> now logging output from csr1000v-2 in logs/csr1000v-2_196E7D86E698.log
	>>> now executing commands from ['show ip route', 'show ip int brief', 'sho logging'] on csr1000v-2
<<< gracefully exited from: csr1000v-2
	>>> now logging output from csr1000v-3 in logs/csr1000v-3_91F885603B1D.log
	>>> now executing commands from ['show ip route', 'show ip int brief', 'sho logging'] on csr1000v-3
<<< gracefully exited from: csr1000v-3
	>>> now logging output from csr1000v-4 in logs/csr1000v-4_E2C17A24952E.log
	>>> now executing commands from ['show ip route', 'show ip int brief', 'sho logging'] on csr1000v-4
<<< gracefully exited from: csr1000v-4
```

### Use an encrypted profile to store common parameters (login, passwords etc...)
```
user@m32e:~/cli-wrapper$ cat profiles/sample
#
--username-credentials
  myLoginAccount
--password
  mySecretPassword
#
user@m32e:~/cli-wrapper$
user@m32e:~/cli-wrapper$ ./cipher.py
What do you wanna do ? decrypt/encrypt - [D/e]: e
What is the filename you want to encrypt ? profiles/sample
Please enter your password: *********
Encrypt "profiles/sample" and save it in "profiles/sample.enc"
user@m32e:~/cli-wrapper$ ./cli.py -f hosts/xrvs -o profiles/sample.enc -cf commands/ipRoutesXr -l
Please enter your password:
        >>> now logging output from xrv1.xyz in logs/xrv1.xyz_6792508A8CDC.log
        >>> now executing commands from ['show route ipv4', 'show route ipv6'] on xrv1.xyz
<<< gracefully exited from: xrv1.xyz
        >>> now logging output from xrv2.xyz in logs/xrv2.xyz_C109B3CDD1B3.log
        >>> now executing commands from ['show route ipv4', 'show route ipv6'] on xrv2.xyz
<<< gracefully exited from: xrv2.xyz
        >>> now logging output from xrv3.xyz in logs/xrv3.xyz_CD502442E225.log
        >>> now executing commands from ['show route ipv4', 'show route ipv6'] on xrv3.yz
<<< gracefully exited from: xrv3.xyz
        >>> now logging output from xrv4.xyz in logs/xrv4.xyz_F48C73F48520.log
        >>> now executing commands from ['show route ipv4', 'show route ipv6'] on xrv4.xyz
<<< gracefully exited from: xrv4.xyz
```

### Use a sub procedure to perform custom actions within a connection (look at "skeleton.py" example in subs directory)
```
user@m32e:~/cli-wrapper$ ./cli.py -f hosts/xrvs -o profiles/sample.enc -s subs.skeleton send_one_comment -v -i
Please enter your password:

csr1000v-1#
csr1000v-1#!
csr1000v-1#!!
csr1000v-1#!!! sample comment...
csr1000v-1#!!
csr1000v-1#!
csr1000v-1#
```
###Use a sub procedure to perform custom actions before the establishment of a connection (look at "second_proxy.py" example in subs directory)
note : if we don't have a 'jumphost' parameter set, the connection does not exist when this procedure is executed.
```
user@m32e:~/cli-wrapper$ ./cli.py -r host -ss subs.second_proxy transparent_connection_to_2nd_proxy
```



### And many other options...
```
user@m32e:~/cli-wrapper$ cli.py -h
usage:
   ./cli.py -r "remote host"| -f "list of hosts" [options]
   ./cli.py -h #get help on numerous options


A small tool to log into any piece of equipment with a decent CLI interface...
You can pass a lot of options to comply with most of devices behavior. Note
that if you ask ./cli.py to look for options in a file, that is "-o" option,
this file obviously contains your credentials, passwords, and thus MUST be
encrypted using the "cipher.py" tool. Enjoy !

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --hosts-file FILE
                        file containing a list of hosts
  -r REMOTE_HOSTNAME, --remote-host REMOTE_HOSTNAME
                        remote host name or IP
  -c COMMAND [COMMAND ...], --command COMMAND [COMMAND ...]
                        command(s) to be executed on remote host
  -cf COMMAND_FILE, --command-file COMMAND_FILE
                        file containing a list of commands
  -d, --debug           debug mode will out in clear all arguments passed to
                        the script
  -i, --interact        switch to interactive mode after connection
  -j LIST [LIST ...], --jumphost-credentials LIST [LIST ...]
                        an ordered list: (protocol,host,port,username,password
                        ,prompt,timeout,verbose) you can omit latest elements
  -l, --logfile         create a logging file in "logs" subdirectory
  -m MORE, --no-more MORE
                        command to pass to remote host to avoid --more-- in
                        execution, defaults to "terminal length 0"
  -o OVERRIDE, --options-override OVERRIDE
                        ciphered file containing arguments that override
                        command line options
  -p PROMPT, --prompt PROMPT
                        expected prompt from remote host
  -po TCP_PORT_NUMBER, --port-number TCP_PORT_NUMBER
                        TCP port number for connection
  -s MODULE METHOD, --sub-proc MODULE METHOD
                        module and function to execute
  -ss MODULE METHOD, --presub-proc MODULE METHOD
                        module and function to execute before connection to
                        remote device
  -t TIMEOUT, --timeout TIMEOUT
                        max seconds to wait for an answer from remote host
  -u USERNAME, --username-credentials USERNAME
                        username to log into remote host
  -v, --verbose         unhide connection process, usefull for debugging
  -w PASSWORD [PASSWORD ...], --password PASSWORD [PASSWORD ...]
                        password to log into remote host and optionally an
                        enable password
  -x {telnet,ssh}, --protocol {telnet,ssh}
                        protocol to be used for connection, defaults to ssh
user@m32e:~/cli-wrapper$
```

## Install
- as an option, install cli-wrapper inside a Python virtualenv to avoid dependancy problems
- grab the package from Github using `git clone` for example
- install it anywhere on your machine
- read `requirements.txt` for a list of Python modules required by the application
  you can use `pip install -r requirements.txt`
- modify environment variables stored in `libs/constants.py` if needed
- keep your setup up to date : `git pull`

## Howto use ?
- simply execute `cli.py --help` from command line, and follow the guidelines
- if you want to store your passwords securely, you should : 
  - put them in a plain text file (see "profiles/sample" or "plaintext" files)
  - cipher the file using `cipher.py` utility with a single password
  - delete the original plain file
  - from now on, you can use `--override` option to inject your credentials into the program

## Features we have
- automation of connection and authentication phases in a secure way
- provide a list of hosts from which we need the same pieces of infos
- provide a list of commands to be executed on a remote host
- comprehensive logging capabilities
- possibility to use a jump server (a server that sits in between us and the targeted host)
- storage of common parameters in local ciphered files
- provide a sub procedure to be customized, so it can execute special actions, depending on interaction with remote host 

## Features that we would need
- a comprehensive documentation set :-)
- let the user provide their own parameters that could be reused in sub procedure
- maybe a testing unit...

## Platforms known to be compatible
- Linux Ubuntu, Debian, Redhat and others for sure but I haven't tested all of them. 
- Cygwin on Windows
- Mac OS

## Remote devices you can log into
Any piece of equipment offering a decent command line interface.  
Note that the expected prompt from the remote device is a regular expression that you can change (-p argument).    
Then the way you interact with the remote device, either manually or automatically, is all yours.   

## Rewards
- Pexpect and Pycryptodome authors and developers
