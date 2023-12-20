# -----------------------------------------------------------
# Cross-check a license file in JSON format with licenses in 
# actual files
#
# (C) 2023 Frank Hofmann, Germany
# email frank.hofmann@efho.de
# License: BSD 3-Clause "New" or "Revised" License
# SPDX-License-Identifier: BSD-3-Clause
# -----------------------------------------------------------

import os, sys
import json
import pprint
import getopt

def displayHelp():
    """display help information"""
    print("""
validate-licenses: cross-check a license file in JSON format with licenses in 
actual files

Options:

  -h, --help: show this help information

  -v, --verbose: enable verbose output (default: disabled)

  -d, --directory: read files from this directory

  -l, --licensefile:  name of the license file
    """)

    # exit 
    sys.exit(0)

# set default values
licenseFile = ""
evaluationDirectory = os.getcwd()
processedFiles = []
licensedFiles = []
verbose = False

# read commandline arguments, first
fullCmdArguments = sys.argv

# - further arguments
argumentList = fullCmdArguments[1:]

# print(fullCmdArguments)

# define possible unix options
unixOptions = "hd:l:v"
gnuOptions = ["help", "directory=", "licensefile=", "verbose"]

try:
    options, arguments = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)

# evaluate given options
for currentOption, currentArgument in options:
    if currentOption in ("-h", "--help"):
        if verbose:
            print ("displaying help")
        displayHelp()
    elif currentOption in ("-v", "--verbose"):
        if verbose:
            print ("enable verbose output")
        verbose = True
    elif currentOption in ("-d", "--directory"):
        if verbose:
            print (("read evaluation directory (%s)") % (currentArgument))
        evaluationDirectory = currentArgument
    elif currentOption in ("-l", "--licensefile"):
        if verbose:
            print (("read name of license file (%s)") % (currentArgument))
        licenseFile = currentArgument

# evaluate set values
# - license file
if not os.path.exists(licenseFile):
    print("cannot open given license file: %s" % licenseFile)
    sys.exit(1)

# - evaluation directory
if not os.path.isdir(evaluationDirectory):
    print("given evaluation directory not accessible: %s" % evaluationDirectory)
    sys.exit(1)

# read data from license file
try:
    licenseFileHandle = open(licenseFile)
    licenseList = json.load(licenseFileHandle)
except:
    print("reading given license file failed: %s" % licenseFile)
    sys.exit(1)

# - check file by file
with os.scandir(evaluationDirectory) as listOfEntries:
    for entry in listOfEntries:
        # output file name
        if entry.is_file():
            currentFile = entry.name
            # extend list of processed files
            processedFiles.append(currentFile)
            # validate file
            if verbose:
                print("processing %s ... " % currentFile)
            if currentFile in licenseList["licenses"]:
                if verbose:
                    print("found %s" % currentFile)
                # extend list of licensed files
                licensedFiles.append(currentFile)

# - discover the filenames that are not in both lists
unlicensedFiles = []     # files that are in the directory but not in license file
unknownFiles = []        # files that are in the license file but in the directory
set1 = set(processedFiles)
set2 = set(licenseList["licenses"])
unlicensedFiles = list(set1.difference(set2))
unknownFiles = list(set2.difference(set1))

# - output validation result
print(" ")
print("files found from the license file:")
for currentFile in licensedFiles:
    print(currentFile)

print(" ")
print("files found that are in the directory but not in license file:")
for currentFile in unlicensedFiles:
    print(currentFile)

print(" ")
print("files found that are in the license file but in the directory:")
for currentFile in unknownFiles:
    print(currentFile)

