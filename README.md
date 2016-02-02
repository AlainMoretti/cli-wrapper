# Cli-wrapper 
##A small project to automate CLI based tasks

>_Because we think CLI is here to stay, at least for troubleshooting purposes_  
>_Because we use it on a daily basis_  
>_Because we were tired of reinventing the wheel..._  

We decided to build this small project using Python and the [pexpect](https://pexpect.readthedocs.org/en/stable/) module. 

##What does cli-wrapper do ? 
###It automates login and let you interact with a remote device
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password -r csr1000v-1  -x telnet

csr1000v-1>
csr1000v-1>q
Connection closed by foreign host.

<<< gracefully exited from: csr1000v-1

user@m32e:~/cli-wrapper$
```
###You can switch to enable mode if you provide a second password
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password enablepassword -r csr1000v-1  -x telnet

csr1000v-1#
csr1000v-1#q
Connection closed by foreign host.

<<< gracefully exited from: csr1000v-1

user@m32e:~/cli-wrapper$
```
###Execute one or several commands on remote device
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
###Send commands output to a log file
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password -r csr1000v-1 -x telnet -c 'sho ip int brief | inc Gi'
  'show ip route' -l
	>>> now logging output from csr1000v-1 in logs/csr1000v-1_D30A74ADA26C.log
	>>> now executing commands from ['sho ip int brief | inc Gi', 'show ip route'] on csr1000v-1

<<< gracefully exited from: csr1000v-1
```
###Send a batch of commands from a file
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
###Send a batch of commands to a list of hosts
```
user@m32e:~/cli-wrapper$ cli.py -u username -w password -f hosts/liste_csr1000v -x telnet -cf commands/sample_
2 -l
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

user@m32e:~/cli-wrapper$
```
###And many other options...
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
  -i, --interact        do not interact after connection
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
amoretti@bytel:~/cli-wrapper$
```

##Install
- grab the package from Github using `git clone` for example
- install it anywhere on your machine
- read `requirements.txt` for a list of Python modules required by the application
  you can use `pip install -r requirements.txt` but PyCrypto install will fail (see known problems below)
- modify environment variables stored in `libs/constants.py` if needed
- keep your setup up to date : `git pull`

##Howto use ?
- simply execute `cli.py --help` from command line, and follow the guidelines
- if you want to store your passwords securely, you should : 
  - put them in a plain text file (see "profiles/sample" or "plaintext" files)
  - cipher the file using `cipher.py` utility with a single password
  - delete the original plain file
  - from now on, you can use `--override` option to inject your credentials into the program

##Features we have
- automation of connection and authentication phases in a secure way
- provide a list of hosts from which we need the same pieces of infos
- provide a list of commands to be executed on a remote host
- comprehensive logging capabilities
- possibility to use a jump server (a server that sits in between us and the targeted host)
- storage of common parameters in local ciphered files
- provide a sub procedure to be customized, so it can execute special actions, depending on interaction with remote host 

##Features that we would need
- a comprehensive documentation set :-)
- let the user provide their own parameters that could be reused in sub procedure
- maybe a testing unit...

##Platforms known to be compatible
- Linux Ubuntu, Debian and others for sure but we haven't tested it yet. 
- Cygwin on Windows

##Known problems
>- there is a bug with PyCrypto install, more details on the [problem](https://github.com/dlitz/pycrypto/issues/108) and a [workaround solution](https://github.com/tootedom/related/blob/master/provisioning/ansible-playground/README.md)
>- sometimes the encrypted profile provided to the "-o" option requires an empty line at the end, 
>  you can figure that out with debug option "-d", and check if the last parameter is not missing.  

##Rewards
- Pexpect and Pcrypto authors and developers
