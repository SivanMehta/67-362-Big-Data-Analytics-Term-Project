import os
from os.path import join
import glob
import json
import re
from pprint import pprint

topdir = '/Users/suave/mprojects/termproject/bills'
exten = '.json'

mdata = {"hconres":{},"hjres":{},"hr":{},"hres":{},"s":{},"sconres":{},
  "sjres":{},"sjres":{},"sres":{}}

def remap():
  for dirpath, dirnames, files in os.walk(topdir):

    for mfile in files:
      file_path = os.path.join(dirpath, mfile)

      if mfile.lower().endswith(exten):

        with open(file_path) as data_file:

          subdir = os.path.basename(os.path.normpath(dirpath))
          num = re.sub("\D", "", subdir)
          key = re.sub("\d", "", subdir)

          ndata = json.load(data_file)
          mdata[key][num] = json.load(data_file)

  # pprint(mdata)
  with open('/Users/suave/mprojects/termproject/map.txt', 'w') as outfile:
    json.dump(mdata, outfile)

remap()