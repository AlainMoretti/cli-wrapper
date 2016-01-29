# Cli-wrapper 
##A small project to automate CLI based tasks

>_Because we thing CLI is here to stay, at least for troubleshooting purposes_  
>_Because we use it on a daily basis_  
>_Because we were tired of reinventing the wheel..._  

We decided to build this small project using Python and the [pexpect](https://pexpect.readthedocs.org/en/stable/) module. 

>Until now, this is just work in progress, first release planned by February 2016.  

##Features we must have
- automation of connection and authentication phases in a secure way
- provide a list of hosts from which we need the same pieces of infos
- provide a list of commands to be executed on a remote host
- comprehensive logging capabilities
- possibility to use a jump server (a server that sits in between us and the targeted host)

##Features that we would need
- provide a sub procedure to be customized, so it can execute special actions, depending on interaction with remote host
- storage of common parameters in local templates, with ability to override some of them if needed 
- let the user provide optional parameters that could be reused in sub procedure
