#!/usr/bin/env python
"""Add Global Exclude Paths to File-based Protection Job Using Python"""

### import pyhesity wrapper module
from pyhesity import *

### command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-j', '--jobname', nargs='+', type=str)

args = parser.parse_args()

jobnames = args.jobname          # name of protection job to add server to
jobnames = [j.lower() for j in jobnames]
for j in jobnames:
    print(j)