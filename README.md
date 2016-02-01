# Cli-wrapper 
##A small project to automate CLI based tasks

>_Because we thing CLI is here to stay, at least for troubleshooting purposes_  
>_Because we use it on a daily basis_  
>_Because we were tired of reinventing the wheel..._  

We decided to build this small project using Python and the [pexpect](https://pexpect.readthedocs.org/en/stable/) module. 

##Install
- grab the package from Github
- install it anywhere on your machine
- read "requirements.txt" for a list of Python modules required by the application

##Howto use ?
- simply execute "cli.py --help" from command line, and follow the guidelines
- if you want to store your passwords securely, you should : 
  - put them in a plain text file (see "profiles/sample" or "plaintext" files)
  - cipher the file using "cipher.py" utility with a single password
  - delete the original plain file
  - from now on, you can use "--override" option to inject your credentials into the program

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

##Rewards
- Pexpect and Pcrypto authors and developers
