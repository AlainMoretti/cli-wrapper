# Cli-wrapper 
##A small project to automate CLI based tasks

Because we thing CLI is here to stay, at least for troubleshooting purposes
Because we use it on a daily basis
Because we were tired of reinventing the wheel...

We decided to build this small project using Python and the [pexpect](https://pexpect.readthedocs.org/en/stable/) module. 

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
