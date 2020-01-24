"""
program to check the virtual memory being used when trying to delete a module

  Created by Ed on 11/14/2019
"""
import sys
import os
import psutil
import pprint

def mem_usage(text):
    process = psutil.Process(os.getpid())
    print(process)
    mem = process.memory_info()[0] / float(2 ** 20)
    print(f'{text}: memory used = {mem}kB')

def mods():
    pprint.pprint(set(sys.modules.keys()) - set(baseModules))


baseModules = sys.modules.keys()

mem_usage('begin')
import re
mem_usage('after import re')
mods()
del re
mem_usage('after del re')
mods()
