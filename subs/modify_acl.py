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

#
# typical command line to launch this procedure would be : 
# cli.py -f hosts/routers -o profiles/myloginandpassword.enc -s subs.modify_acl add_stats_per_entry
# cli.py -f hosts/routers -o profiles/myloginandpassword.enc -s subs.modify_acl add_deny_statement
#
# The expected result is :
# - connect to each router of "routers"
# - check if any ACL is configured 
# - modify it according to the method
#
#we can perform any conditional action inside this block of code
def add_stats_per_entry(args,c):
    #check if the router has some ACL with name containing 'FROM'
    c.sendline('show ip access-list | inc FROM')
    c.expect(args.prompt)
    #grab and parse the output
    out = c.before
    outlist = out.split("\n")
    #go to configuration mode
    c.sendline('configure')
    c.expect(args.prompt)
    for line in outlist:
        if line[0:14] == 'IP access list':
            #now iterate over any ACL and apply the change
            c.sendline("ip access-list "+line[15:])
            c.expect(args.prompt)
            c.sendline("statistics per-entry")
            c.expect(args.prompt)
    c.sendline('end')
    c.expect(args.prompt) 

def add_deny_statement(args,c):
    #check if the router has some ACL with name containing 'FROM'
    c.sendline('show ip access-list | inc FROM')
    c.expect(args.prompt)
    #grab and parse the output
    out = c.before
    outlist = out.split("\n")
    #go to configuration mode
    c.sendline('configure')
    c.expect(args.prompt)
    for line in outlist:
        if line[0:14] == 'IP access list':
            #now iterate over any ACL and apply the change
            c.sendline("ip access-list "+line[15:])
            c.expect(args.prompt)
            c.sendline("deny ip any any log")
            c.expect(args.prompt)
    c.sendline('end')
    c.expect(args.prompt) 

def main():
    print "\n\n>>>>> this module is used as a parameter of main program, it does nothing by itself <<<<<<<<<\n\n"

if __name__ == "__main__":
    main()
