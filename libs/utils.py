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

import os
from libs import constants

def BuildLogfile(h):
    if not os.path.isdir(constants.LOGDIR):
        print('INFO: create a folder '+constants.LOGDIR+' to store logging files')
        os.makedirs(constants.LOGDIR)
    if constants.LOGFILE_NAME == 'RANDOM_STRING':
        import random
        logname = ('%12x' % random.randrange(16**12)).upper()
    elif constants.LOGFILE_NAME == 'DATE':
        import datetime
        logname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    else:exit('ERROR: '+constants.LOGFILE_NAME+' is not an expected value for constant "LOGFILE_NAME"...')
    logfile = constants.LOGDIR+'/'+h+'_'+logname+'.log' 
    return logfile 

def CleanComments(array):
    cleaning = False
    for i, item in enumerate(array):
        if item[0] == '#':
            array[i] = ''
            cleaning = True
    array = [x.strip(' ') for x in array]
    remove = True
    while remove:
        try:
            array.remove('')
        except:remove = False
    return array