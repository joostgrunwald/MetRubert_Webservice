#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- CLAM Wrapper script Template --
#       by Maarten van Gompel (proycon)
#       https://proycon.github.io/clam
#       Centre for Language and Speech Technology
#       Radboud University Nijmegen
#
#       (adapt or remove this header for your own code)
#
#       Licensed under GPLv3
#
###############################################################

#This is a template wrapper which you can use a basis for writing your own
#system wrapper script. The system wrapper script is called by CLAM, it's job it
#to call your actual tool.

#This script will be called by CLAM and will run with the current working directory set to the specified project directory

#This wrapper script uses Python and the CLAM Data API.
#We make use of the XML settings file that CLAM outputs, rather than
#passing all parameters on the command line.


#import some general python modules:
import sys
import os
import codecs
import re
import string
import glob
import traceback

#import CLAM-specific modules. The CLAM API makes a lot of stuff easily accessible.
import clam.common.data
import clam.common.status

from natsort import natsorted
from foliatools import alpino2folia
from metaphorclam import CUSTOM_FORMATS


#imports used for file replacements
import fnmatch

#import our own parser
import pasmaparser_cov_melBert_allpos_clam as parser

import pathlib
#import our own model
from MetRuBert_production import main_dutch

#import our own output prettifier
import outputgenerator as outputgen

#When the wrapper is started, the current working directory corresponds to the project directory, input files are in input/ , output files should go in output/ .

#make a shortcut to the shellsafe() function
shellsafe = clam.common.data.shellsafe

#this script takes three arguments from CLAM: $DATAFILE $STATUSFILE $OUTPUTDIRECTORY
#(as configured at COMMAND= in the service configuration file, there you can
#reconfigure which arguments are passed and in what order.
datafile = sys.argv[1]
statusfile = sys.argv[2]
outputdir = sys.argv[3]
#arguments = sys.argv[4]
ALPINO_HOME = sys.argv[4]

#If you make use of CUSTOM_FORMATS, you need to import your service configuration file here and set clam.common.data.CUSTOM_FORMATS
#Moreover, you can import any other settings from your service configuration file as well:

#from yourserviceconf import CUSTOM_FORMATS
#clam.common.data.CUSTOM_FORMATS = CUSTOM_FORMATS

#Obtain all data from the CLAM system (passed in $DATAFILE (clam.xml)), always pass CUSTOM_FORMATS as second argument if you make use of it!
clamdata = clam.common.data.getclamdata(datafile)

#You now have access to all data. A few properties at your disposition now are:
# clamdata.system_id , clamdata.project, clamdata.user, clamdata.status , clamdata.parameters, clamdata.inputformats, clamdata.outputformats , clamdata.input , clamdata.output

clam.common.status.write(statusfile, "Starting...")


#-- EXAMPLE B: Iterate over all input files? --

# This example iterates over all input files, it can be a simpler
# method for setting up your wrapper:

########################################################
# WE LOAD PARAMETER DECLARATIONS INTO PYTHON VARIABLES #
########################################################

################
# POS PARAMETERS

#get actual yes/no values from parameters
noun = clamdata['noun']
verb = clamdata['verb']
adj = clamdata['adj']
adv = clamdata['adv']
pron = clamdata['pron']
det = clamdata['det']
num = clamdata['num']

#use parameter values to create a parameter list
pos_list = []
if str(noun) == "no":
   pos_list.append("noun")
if str(verb) == "no":
   pos_list.append("verb")
if str(adj) == "no":
   pos_list.append("adj")
if str(adv) == "no":
   pos_list.append("adv")
if str(pron) == "no":
   pos_list.append("pron")
if str(det) == "no":
   pos_list.append("det")
if str(num) == "no":
   pos_list.append("num")

###################
# OUTPUT PARAMETERS

#get actual yes/no values from parameters
alp = clamdata['alp']
tok = clamdata['tok']
sof = clamdata['sof']
unres = clamdata['unres']
sof2 = clamdata['sof2']

##########################################
# WE CHECK IF WE RECEIVED A DEV.TSV FILE #
##########################################

#get template of last input item (should be only one input in case of dev.tsv file)
inputfile = ""

input_files = 0
stop_iteration = False
alpino_files = True

for inputfile in clamdata.input:
    input_files = input_files + 1
    if ".tsv" in str(inputfile) and input_files > 1:
        clam.common.status.write(statusfile, "ERROR, DEV FILE BUT MORE THEN ONE INPUT")
        stop_iteration = True
    if ".xml" in str(inputfile):
        alpino_files = False

if stop_iteration == False and str(inputfile).find(".tsv") != -1:
    # ! CASE 1: SINGLE DEV FILE SUPPLIED

    dev_path = ""
    for devfile in clamdata.input:
        dev_path = str(devfile)

    #update program status
    clam.common.status.write(statusfile, "Running MetRobert on dev.tsv file")

    #run the dutch model on the dev file
    main_dutch.main(dev_path)

    #update program status
    clam.common.status.write(statusfile, "Creating output.tsv table")

    #prettify the output
    outputgen.main(outputdir, pos_list, False, dev_path, sof2)

    #cleanup
    for file in os.listdir(outputdir):
        if file.endswith("dev_float.txt") and str(unres) == "no":
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)
        elif file.endswith("dev_soft.txt") and str(sof) == "no":
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)
        elif file.endswith("_dev2.txt") or file.endswith("dev2.tsv") or file.endswith("soft2.txt"):
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)

elif str(inputfile).find(".xml") != -1:
    # ! CASE 2: ALPINO FILES SUPPLIED

    #update program status
    clam.common.status.write(statusfile, "Generating dev.tsv data for model")
    print("generating dev.tsv data for model")

    #get location needed
    dev_location = outputdir.replace("output","input")

    #run the python file to generate dev data
    parser.main(dev_location)

    #go to directory where dev.tsv data was created
    os.chdir(dev_location)

    #update program status
    clam.common.status.write(statusfile, "Cleaning up alpino .xml files")
    print("Cleaning up alpino xml files")

    #cleanup folders unneeded xml files
    for direc in os.listdir(dev_location):
        d = os.path.join(dev_location, direc)
        if os.path.isdir(d):
            print("cleaning folder" + str(d))
            for file in os.listdir(d):
                if file.endswith(".xml") and str(alp) == "no":
                    try:
                        os.remove(d + "/" + file)
                    except:
                        print("Error while deleting xml file : ", file)

    #get location of dev file to copy
    dev_file = dev_location + "/" + "dev.tsv"

    #update program status
    clam.common.status.write(statusfile, "Running MetRobert on dev.tsv file")

    #run the dutch model on the dev file
    main_dutch.main(dev_file)

    #update program status
    clam.common.status.write(statusfile, "Creating output.tsv table")

    #prettify the output
    outputgen.main(outputdir, pos_list, True, None, sof2)

    #cleanup
    for file in os.listdir(outputdir):
        if file.endswith(".tok") and str(tok) == "no":
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)
        elif file.endswith("dev_float.txt") and str(unres) == "no":
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)
        elif file.endswith("dev_soft.txt") and str(sof) == "no":
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)
        elif file.endswith("_dev2.txt") or file.endswith("dev2.tsv") or file.endswith("soft2.txt"):
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)


elif str(inputfile).find(".tsv") == -1 and str(inputfile).find(".xml") == -1 and str(inputfile).find(".txt") != -1:
    # ! CASE 3: SENTENCE FILES SUPPLIED

    ##################################
    # WE CLEAN UP THE INPUT SENTENCES#
    ##################################

    #Update user interface log
    #clam.common.status.write(statusfile, "Fixing input files...")

    #Replace all quotation marks in files
    #findReplace(outputdir.replace("output","input"), "*.txt") 
    #findReplace(outputdir.replace("output","input"), "*.tok")

    #helper function for file replacements
    def findReplace(directory, filePattern):
        for path, dirs, files in os.walk(os.path.abspath(directory)):
            for filename in fnmatch.filter(files, filePattern):
                filepath = os.path.join(path, filename)
                s = pathlib.Path(filepath).read_text()
                
                if s[:2] == "' ":
                    s = s.replace("' ","'", 1)

                #extra checks added
                s = s.replace("''", "")
                s = s.replace(" ,,", " ")
                s = s.replace(",,", " ")
                s = s.replace("\"", "")
                s = s.replace(" , ", ", ")
                s = s.replace(" \\ ", "\\")
                s = s.replace(" / ", "/")
                s = s.replace(" :", ":")
                s = s.replace(",, ", "")

                #second round of extra checks
                s = s.replace(", ,", "")
                s = s.replace(" ?", "?")
                s = s.replace(" - ","- ")

                #third round of extra checks
                s = s.replace(" ( "," (")
                s = s.replace(" ) ", ") ")
                s = s.replace(" . ", ". ")

                s = s.replace(" ',","',")
                s = s.replace(" '',","'',")

                s = s.replace(" ' ", " '", 1)
                s = s.replace(" ' ", "' ", 1)
                s = s.replace(" ' ", " '", 1)
                s = s.replace(" ' ", "' ", 1)
                s = s.replace(" ' ", " '", 1)
                s = s.replace(" ' ", "' ", 1)
                s = s.replace(" ' ", " '", 1)
                s = s.replace(" ' ", "' ", 1)
                with open(filepath, "w") as f:
                    f.write(s)

    #################################
    # WE USE ALPINO ON ALL OUR FILES#
    #################################

    for inputfile in clamdata.input:

        inputtemplate = inputfile.metadata.inputtemplate
        inputfilepath = str(inputfile)
        basename = os.path.basename(inputfilepath)[:-4] #without extension

        #? CASE: UNTOKENIZED
        if inputtemplate == 'untokinput':
            #we have to tokenize first
            clam.common.status.write(statusfile, "Tokenizing " + basename)
            tokfile = os.path.join(outputdir,basename + '.tok')
            r = os.system('ucto -L nl -n ' + shellsafe(inputfilepath,'"') + ' > ' + shellsafe(tokfile,'"'))
            if r != 0:
                print("Failure running ucto",file=sys.stderr)
                sys.exit(2)

            #Replace all quotation marks in files
            findReplace(outputdir, "*.txt") 
            findReplace(outputdir, "*.tok")

        #? CASE: TOKENISED
        else:
            tokfile = os.path.abspath(inputfilepath)
            os.system("sed -i 's/^M$//' " + shellsafe(tokfile,'"'))  #convert nasty DOS end-of-line to proper unix

            #Replace all quotation marks in files
            findReplace(outputdir.replace("output","input"), "*.txt") 
            findReplace(outputdir.replace("output","input"), "*.tok")

        clam.common.status.write(statusfile, "Running Alpino on " + basename)

        pwd = os.getcwd()
        os.chdir(outputdir)
        if not os.path.exists("xml"):
            os.mkdir("xml")
        else:
            for filename in glob.glob('xml/*.xml'):
                os.unlink(filename) #clear for next round

        cmd = "ALPINO_HOME=" + shellsafe(ALPINO_HOME) + " " + ALPINO_HOME + "/bin/Alpino -veryfast -flag treebank xml debug=1 end_hook=xml user_max=900000 -parse < "  + tokfile
        print(cmd,file=sys.stderr)
        r = os.system(cmd)
        if r != 0:
            print("Failure running alpino",file=sys.stderr)
            sys.exit(2)

        os.chdir("xml")

        os.chdir('..')
        os.rename('xml','xml_' + basename)
        os.chdir(pwd)

    #######################################
    #SECONDLY WE GENERATE OUR DEV.TSV DATA#
    #######################################

    #update program status
    clam.common.status.write(statusfile, "Generating dev.tsv data for model")
    print("generating dev.tsv data for model")

    #get location needed
    dev_location = outputdir

    #run the python file to generate dev data
    parser.main(dev_location)

    #go to directory where dev.tsv data was created
    os.chdir(dev_location)

    #update program status
    clam.common.status.write(statusfile, "Cleaning up alpino .xml files")
    print("Cleaning up alpino xml files")

    #cleanup folders unneeded xml files
    for dire in os.listdir(dev_location):
        d = os.path.join(dev_location, dire)
        if os.path.isdir(d):
            print("cleaning folder" + str(d))
            for file in os.listdir(d):
                if file.endswith(".xml") and str(alp) == "no":
                    try:
                        os.remove(d + "/" + file)
                    except:
                        print("Error while deleting xml file : ", file)

    #get location of dev file to copy
    dev_file = dev_location + "/" + "dev.tsv"
    print(dev_file)

    #update program status
    clam.common.status.write(statusfile, "Running MetRobert on dev.tsv file")

    #run the dutch model on the dev file
    main_dutch.main(dev_file)

    #update program status
    clam.common.status.write(statusfile, "Generating output.tsv file")

    #prettify output
    outputgen.main(outputdir, pos_list, True, None, sof2)

    #cleanup
    for file in os.listdir(outputdir):
        if file.endswith(".tok") and str(tok) == "no":
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deteling tok file : ", file)
        elif file.endswith("dev_float.txt") and str(unres) == "no":
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)
        elif file.endswith("dev_sof.txt") and str(sof) == "no":
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)
        elif file.endswith("_dev2.txt") or file.endswith("dev2.tsv") or file.endswith("soft2.txt"):
            try:
                os.remove(outputdir + "/" + file)
            except:
                print("Error while deleting tok file : ", file)

#we clean empty folders inside our output directory
def remove_empty_folders(path_abs):
    walk = list(os.walk(path_abs))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            os.rmdir(path)

remove_empty_folders(outputdir)



#for inputfile in clamdata.input:
#   inputtemplate = inputfile.metadata.inputtemplate
#   inputfilepath = str(inputfile)
#   encoding = inputfile.metadata['encoding'] #Example showing how to obtain metadata parameters

#(Note: Both these iteration examples will fail if you change the current working directory, so make sure to set it back to the initial path if you do need to change it!!)

#-- EXAMPLE C: Grab a specific input file? (by input template) --

# Iteration over all input files is often not necessary either, you can just do:

#inputfile = clamdata.inputfile('replace-with-inputtemplate-id')
#inputfilepath = str(inputfile)

#========================================================================================

# Below is an example of how to read global parameters and how to invoke your
# actual system. You may want to integrete these into one of the solution
# examples A,B or C above.

#-- Read global parameters? --

# Global parameters are accessed by addressing the clamdata instance as-if were a simple dictionary.

#parameter = clamdata['parameter_id']

#-- Invoke your actual system? --

# note the use of the shellsafe() function that wraps a variable in the
# specified quotes (second parameter) and makes sure the value doesn't break
# out of the quoted environment! Can be used without the quote too, but will be
# do much stricter checks then to ensure security.

#os.system("system.pl " + shellsafe(inputfilepath,'"') );

# Rather than execute a single system, call you may want to invoke it multiple
# times from within one of the iterations.

#A nice status message to indicate we're done
clam.common.status.write(statusfile, "Done",100) # status update

sys.exit(0) #non-zero exit codes indicate an error and will be picked up by CLAM as such!
