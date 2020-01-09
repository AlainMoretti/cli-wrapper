# Copyright 2016 Netfishers
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.




# Here below some examples that you could use to build your own subs
# note that we always provide 2 arguments: 
# - args is the object containing all arguments passed to the script, ie: the actual argparse object
# - c is the connection, ie: the actual Pexpect object 

# Because you have total control of what you do with output from actions taken by a sub, 
# it is executed before all other arguments passed to the script (commands, interaction, and so on)
# That means that you will not see anything out to screen by default, unless:
# - you pass the '-v' argument
# - you ask the sub to print explicitely something 


# you could try to call the 'does_nothing' method to see if your sub is correctly executed 
# this does nothing except print the below message
# typical command line to launch this procedure would be : 
# cli.py -f hosts/routers -o profiles/myloginandpassword.enc -s subs.skeleton does_nothing
def does_nothing(args,c):
    print ("\n\n>>>>> now entering in a subprocess and execute some additional and custom commands <<<<<<<<<\n\n")



# the following method will out the comprehensive content of both 'args' and 'c' objects
# be careful: your passwords will out in clear text !!
# typical command line to launch this procedure would be : 
# cli.py -f hosts/routers -o profiles/myloginandpassword.enc -s subs.skeleton get_env_variables
def get_env_variables(args,c):
    import pprint
    print('here below the variables that you can use inside your custom functions: ')
    print('The "args" object:')
    pprint.pprint(vars(args))
    print('The "c" object:')
    pprint.pprint(vars(c))

    
# the following method is pretty simple and useless: 
# it interacts with the actual connection, print a comment, and then return control to the main loop
# typical command line to launch this procedure would be : 
# cli.py -f hosts/routers -o profiles/myloginandpassword.enc -s subs.skeleton send_one_comment -v
def send_one_comment(args,c):
    c.sendline('!')
    c.expect(args.prompt)
    c.sendline('!!')
    c.expect(args.prompt)
    c.sendline('!!! kinda useless comment...')
    c.expect(args.prompt)
    c.sendline('!!')
    c.expect(args.prompt)
    c.sendline('!')
    c.expect(args.prompt)
 

def main():
    print ("\n\n>>>>> this module is used as a parameter to the main program, it does nothing by itself <<<<<<<<<\n\n")
        
if __name__ == "__main__":
    main()