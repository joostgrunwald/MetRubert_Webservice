#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Service Configuration File (Template) --
#       by Maarten van Gompel (proycon)
#       Centre for Language and Speech Technology / Language Machines
#       Radboud University Nijmegen
#
#       https://proycon.github.io/clam
#
#       Licensed under GPLv3
#
###############################################################

#Consult the CLAM manual for extensive documentation

from clam.common.parameters import *
from clam.common.formats import *
from clam.common.converters import *
from clam.common.viewers import *
from clam.common.data import *
from clam.common.digestauth import pwhash
import clam
import sys
import os

REQUIRE_VERSION = 3.0

CLAMDIR = clam.__path__[0] #directory where CLAM is installed, detected automatically
WEBSERVICEDIR = os.path.dirname(os.path.abspath(__file__)) #directory where this webservice is installed, detected automatically

# ======== GENERAL INFORMATION ===========

# General information concerning your system.


#The System ID, a short alphanumeric identifier for internal use only (mandatory!)
SYSTEM_ID = "metaphorclam"
#System name, the way the system is presented to the world
SYSTEM_NAME = "MetRobert"

#An informative description for this system (this should be fairly short, about one paragraph, and may not contain HTML)
SYSTEM_DESCRIPTION = "MetRobert is a metaphor detection model for Dutch and English, it is developed by Joost Grunwald at the Radboud University Nijmegen. It will automaticly try to predict metaphors in text. You can upload either tokenized or untokenized files (which will be automaticly tokenized for you using ucto), the output will consist of a .tsv file used for the input of the model and of the predictions before and after softmax and boolean conversion have been applied. We also deliver a file with save test inputs."

#A version label of the underlying tool and/or this CLAM wrapper
#(If you can derive this dynamically then that is strongly recommended!)
SYSTEM_VERSION = 0.2

#The author(s) of the underlying tool and/or this CLAM wrapper
#(If you can derive this dynamically then that is strongly recommended!)
SYSTEM_AUTHOR = "Joost Grunwald"

#How to reach the authors?
SYSTEM_EMAIL = "s1057493@ru.nl"

#What license do we want
SYSTEM_LICENSE = "GNU general public license 3.0"

#some settings of the interface
INTERFACEOPTIONS = "centercover,coverheight100"

#Does this system have a homepage (or possibly a source repository otherwise)
#SYSTEM_URL = ""

#Is this webservice embedded in a larger system? Like part of an institution or particular portal site. If so, mention the URL here.
#SYSTEM_PARENT_URL = ""

#The URL of a cover image to prominently display in the header of the interface. You may also want to set INTERFACEOPTIONS="centercover" to center it horizontally.
#SYSTEM_COVER_URL = ""

#URL to a website where users can register an account for use with this webservice. This link is only for human end
#users, not an API endpoint.
#SYSTEM_REGISTER_URL = ""
SWITCHBOARD_FORWARD_URL = None
FROG_FORWARD_URL = None
FLATURL = None

if 'ALPINO_HOME' in os.environ:
    ALPINO_HOME = os.environ['ALPINO_HOME']

# ======== LOCATION ===========

#Either add a section for your host here, or
#specify these variables in an external yaml file
#called $hostname.yaml or config.yaml and use the loadconfig() mechanism.
#Such an external file will be looked for my default and is the recommended way.

host = os.uname()[1]
if host == "yourhostname":
    #The root directory for CLAM, all project files, (input & output) and
    #pre-installed corpora will be stored here. Set to an absolute path:
    ROOT = "/tmp/clam.projects/"

    #The URL of the system (If you start clam with the built-in webserver, you can override this with -P)
    PORT= 8080

    #The hostname of the system. Will be automatically determined if not set. (If you start clam with the built-in webserver, you can override this with -H)
    #Users *must* make use of this hostname and no other (even if it points to the same IP) for the web application to work.
    HOST = 'yourhostname'

    #If the webservice runs in another webserver (e.g. apache, nginx, lighttpd), and it
    #doesn't run at the root of the server, you can specify a URL prefix here:
    #URLPREFIX = "/myservice/"

    #If you run behind a reverse proxy, you can autodetect your host if you run
    #if your reverse proxy properly sets the X-Forwarded-Host and X-Forwarded-Proto headers.
    #Setting this when you are NOT behind a reverse proxy that output these headers, is a security risk:
    #USE_FORWARDED_HOST = False

    #Alternatively to the above, you can force the full URL CLAM has to use, rather than rely on any autodetected measures:
    #FORCEURL = "http://yourhostname.com"

    # ======== AUTHENTICATION & SECURITY ===========

    #Users and passwords

    #set security realm, a required component for hashing passwords (will default to SYSTEM_ID if not set)
    #REALM = SYSTEM_ID

    #USERS = None #no user authentication/security (this is not recommended for production environments!)
    #If you want to enable user-based security, you can define a dictionary
    #of users and (hashed) passwords here. The actual authentication will proceed
    #as HTTP Digest Authentication. Although being a convenient shortcut,
    #using pwhash and plaintext password in this code is not secure!!

    USERS = {
    
    }

    #List of usernames that are administrator and can access the administrative web-interface (on URL /admin/)
    ADMINS = {
	    
    }

else:
    #This invokes the automatic loader, do not change it;
    #it will try to find a file named $system_id.$hostname.yml or just $hostname.yml, where $hostname
    #is the auto-detected hostname of this system. Alternatively, it tries a static $system_id.config.yml or just config.yml .
    #You can also set an environment variable CONFIGFILE to specify the exact file to load at run-time.
    #It will look in several paths including the current working directory and the path this settings script is loaded from.
    #Such an external configuration file simply defines variables that will be imported here. If it fails to find
    #a configuration file, an exception will be raised.
    loadconfig(__name__)





#Amount of free memory required prior to starting a new process (in MB!), Free Memory + Cached (without swap!). Set to 0 to disable this check (not recommended)
#REQUIREMEMORY = 10

#Maximum load average at which processes are still started (first number reported by 'uptime'). Set to 0 to disable this check (not recommended)
#MAXLOADAVG = 4.0

#Minimum amount of free diskspace in MB. Set to 0 to disable this check (not recommended)
#DISK = '/dev/sda1' #set this to the disk where ROOT is on
#MINDISKSPACE = 10

#The amount of diskspace a user may use (in MB), this is a soft quota which can be exceeded, but creation of new projects is blocked until usage drops below the quota again
#USERQUOTA = 100

#The secret key is used internally for cryptographically signing session data, in production environments, you'll want to set this to a persistent value. If not set it will be randomly generated.
#SECRET_KEY = 'mysecret'

#Allow Asynchronous HTTP requests from **web browsers** in following domains (sets Access-Control-Allow-Origin HTTP headers), by default this is unrestricted
#ALLOW_ORIGIN = "*"

# ======== WEB-APPLICATION STYLING =============

#Choose a style (has to be defined as a CSS file in clam/style/ ). You can copy, rename and adapt it to make your own style
STYLE = 'style_joost'

# ======== ENABLED FORMATS ===========

#In CUSTOM_FORMATS you can specify a list of Python classes corresponding to extra formats.
#You can define the classes first, and then put them in CUSTOM_FORMATS, as shown in this example:

class MetRobertXMLFormat(CLAMMetaData):
    attributes = {}
    name = "MetRobert XML collection"
    mimetype = 'application/zip'

CUSTOM_FORMATS = [ MetRobertXMLFormat ]

# ======== ENABLED VIEWERS ===========

#In CUSTOM_VIEWERS you can specify a list of Python classes corresponding to extra viewers.
#You can define the classes first, and then put them in CUSTOM_VIEWERS, as shown in this example:

# CUSTOM_VIEWERS = [ MyXMLViewer ]

# ======= INTERFACE OPTIONS ===========

#Here you can specify additional interface options (space separated list), see the documentation for all allowed options
#INTERFACEOPTIONS = "inputfromweb" #allow CLAM to download its input from a user-specified url

# ======== PROJECTS: PREINSTALLED DATA ===========

#INPUTSOURCES = [
#    InputSource(id='sampledocs',label='Sample texts',path=ROOT+'/inputsources/sampledata',defaultmetadata=PlainTextFormat(None, encoding='utf-8') ),
#]

# ======== PROJECTS: PROFILE DEFINITIONS ===========

#Define your profiles here. This is required for the project paradigm, but can be set to an empty list if you only use the action paradigm.-
PROFILES = [
    Profile(
        InputTemplate('tokinput', PlainTextFormat,"Plaintext tokenised input, one sentence per line",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            extension='.tok',
            multi=True
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('alpinooutput',MetRobertXMLFormat,'Alpino XML output (XML files per sentence)',
            extension='.alpinoxml.zip', #set an extension or set a filename:
            removeextension='.tok',
            multi=True,
        ),
        OutputTemplate('foliaoutput',FoLiAXMLFormat,'FoLiA XML Output',
            FoLiAViewer(),
            ForwardViewer(id='switchboardforwarder',name="Open in CLARIN Switchboard",forwarder=Forwarder('switchboard','CLARIN Switchboard',SWITCHBOARD_FORWARD_URL),allowdefault=False) if SWITCHBOARD_FORWARD_URL else None,
            ForwardViewer(id='frogforwarder',name="Continue with Frog",forwarder=Forwarder('frog','Frog',FROG_FORWARD_URL)) if FROG_FORWARD_URL else None,
            extension='.folia.xml', #set an extension or set a filename:
            removeextension='.tok',
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('untokinput', PlainTextFormat,"Plaintext document (untokenised)",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #MSWordConverter(id='docconv',label='Convert from MS Word Document'),
            extension='.txt',
            multi=True, #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('tokoutput', PlainTextFormat,"Plaintext tokenised output, one sentence per line",
            SetMetaField('encoding','utf-8'),
            ForwardViewer(id='switchboardforwarder',name="Open in CLARIN Switchboard",forwarder=Forwarder('switchboard','CLARIN Switchboard',SWITCHBOARD_FORWARD_URL),allowdefault=False) if SWITCHBOARD_FORWARD_URL else None,
            removeextensions='.txt',
            extension='.tok',
            multi=True,
        ),
        OutputTemplate('alpinooutput',MetRobertXMLFormat,'Alpino XML output (XML files per sentence)',
            extension='.alpinoxml.zip', #set an extension or set a filename:
            removeextensions='.txt',
            multi=True,
        ),
        OutputTemplate('foliaoutput',FoLiAXMLFormat,'FoLiA XML Output',
            FoLiAViewer(),
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            ForwardViewer(id='switchboardforwarder',name="Open in CLARIN Switchboard",forwarder=Forwarder('switchboard','CLARIN Switchboard',SWITCHBOARD_FORWARD_URL),allowdefault=False) if SWITCHBOARD_FORWARD_URL else None,
            ForwardViewer(id='frogforwarder',name="Continue with Frog",forwarder=Forwarder('frog','Frog',FROG_FORWARD_URL)) if FROG_FORWARD_URL else None,
            extension='.folia.xml', #set an extension or set a filename:
            removeextension='.txt',
            multi=True,
        ),
    ),

    #Profile(
     #   InputTemplate('devinput', PlainTextFormat,"Dev.tsv training file (For rerunning the model)",
      #      StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #MSWordConverter(id='docconv',label='Convert from MS Word Document'),
       #     extension='.tsv',
        #    unique=True,
             #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
       # ),
        #------------------------------------------------------------------------------------------------------------------------
       # OutputTemplate('modeloutput',PlainTextFormat,'Predictions and analysis from the model',
       #     extension='.txt', #set an extension or set a filename:
       #     unique=True,
       # ),
       # OutputTemplate('devfile',PlainTextFormat,'The generated dev.tsv files',
       #     extension='.tsv', #set an extension or set a filename:
       #     unique=True,
       # ),
   # ),
   # Profile(
      #  InputTemplate('alpinoinput', PlainTextFormat,"Alpino .xml files (For rerunning the model)",
          #  StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #MSWordConverter(id='docconv',label='Convert from MS Word Document'),
         #   extension='.xml',
        #    unique=True, #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
       # ),
        #------------------------------------------------------------------------------------------------------------------------
       # OutputTemplate('modeloutput',PlainTextFormat,'Predictions and analysis from the model',
       #     extension='.txt', #set an extension or set a filename:
       #     unique=True,
       # ),
       # OutputTemplate('devfile',PlainTextFormat,'The generated dev.tsv files',
       #     extension='.tsv', #set an extension or set a filename:
       #     unique=True,
       # ),

   # )

]

# ======== PROJECTS: COMMAND ===========

#The system command for the project paradigm.
#It is recommended you set this to small wrapper
#script around your actual system. Full shell syntax is supported. Using
#absolute paths is preferred. The current working directory will be
#set to the project directory.
#
#You can make use of the following special variables,
#which will be automatically set by CLAM:
#     $INPUTDIRECTORY  - The directory where input files are uploaded.
#     $OUTPUTDIRECTORY - The directory where the system should output
#                        its output files.
#     $TMPDIRECTORY    - The directory where the system should output
#                        its temporary files.
#     $STATUSFILE      - Filename of the .status file where the system
#                        should output status messages.
#     $DATAFILE        - Filename of the clam.xml file describing the
#                        system and chosen configuration.
#     $USERNAME        - The username of the currently logged in user
#                        (set to "anonymous" if there is none)
#     $PARAMETERS      - List of chosen parameters, using the specified flags
#
COMMAND = WEBSERVICEDIR + "/metaphorclam_wrapper.py $DATAFILE $STATUSFILE $OUTPUTDIRECTORY " + ALPINO_HOME
print("COMMAND")
print(COMMAND)
#Or for the shell variant:
#COMMAND = WEBSERVICEDIR + "/metaphorclam_wrapper.sh $STATUSFILE $INPUTDIRECTORY $OUTPUTDIRECTORY $PARAMETERS"

#Or if you only use the action paradigm, set COMMAND = None

# ======== PARAMETER DEFINITIONS ===========

#The global parameters (for the project paradigm) are subdivided into several
#groups. In the form of a list of (groupname, parameters) tuples. The parameters
#are a list of instances from common/parameters.py

#PARAMETERS = []
PARAMETERS =  [
    ('POS TAGS', [   #change or comment this
        #BooleanParameter(id='createlexicon',name='Create Lexicon',description='Generate a separate overall lexicon?'),
        ChoiceParameter(id='noun',name='Noun Prediction',description='Enable predictions of metaphors for nouns?', choices=['yes','no'],default='yes'),
        ChoiceParameter(id='verb',name='Verb Prediction',description='Enable predictions of metaphors for verbs?', choices=['yes','no'],default='yes'),
        ChoiceParameter(id='adv',name='Adverb Prediction',description='Enable predictions of metaphors for adverbs?', choices=['yes','no'],default='yes'),
        ChoiceParameter(id='adj',name='Adjective Prediction',description='Enable predictions of metaphors for adjectives?', choices=['yes','no'],default='yes'),
        ChoiceParameter(id='det',name='Determinant Prediction',description='Enable predictions of metaphors for determinants?', choices=['yes','no'],default='yes'),
        ChoiceParameter(id='pron',name='Pronoun Prediction',description='Enable predictions of metaphors for pronouns?', choices=['yes','no'],default='yes'),
        ChoiceParameter(id='num',name='Number Prediction',description='Enable predictions of metaphors for numbers?', choices=['yes','no'],default='yes'),

        #StringParameter(id='author',name='Author',description='Sign output metadata with the specified author name',maxlength=255),
    ] ),
    ('OUTPUT FILES', [ # change or comment this
        ChoiceParameter(id='alp',name='Alpino output',description='Save the output of Alpino and return it to user?', choices=['yes','no'],default='no'),
        ChoiceParameter(id='tok',name='Ucto output',description='Save the output of Ucto and return it to user?', choices=['yes','no'],default='no'),
        ChoiceParameter(id='unres',name='Unedited output',description='Save the pure output of the model and return it to user?', choices=['yes','no'],default='no'),
        ChoiceParameter(id='sof',name='Softmax file',description='Save the softmax file output of the model and return it to user?', choices=['yes','no'],default='yes'),
        ChoiceParameter(id='sof2',name='Softmax output',description='Save the softmax outputs inside the output.tsv files?', choices=['yes','no'],default='yes'),
    ] )

]


# ======= ACTIONS =============

#The action paradigm is an independent Remote-Procedure-Call mechanism that
#allows you to tie scripts (command=) or Python functions (function=) to URLs.
#It has no notion of projects or files and must respond in real-time. The syntax
#for commands is equal to those of COMMAND above, any file or project specific
#variables are not available though, so there is no $DATAFILE, $STATUSFILE, $INPUTDIRECTORY, $OUTPUTDIRECTORY or $PROJECT.

ACTIONS = [
    #Action(id='multiply',name='Multiply',parameters=[
    #    IntegerParameter(id='x',name='Value'),
    #    IntegerParameter(id='y',name='Multiplier'),
    #   ],
    #   command=sys.path[0] + "/actions/multiply.sh $PARAMETERS"
    #   tmpdir=False,     #if your command writes intermediate files, you need to set this to True i
                          #(or to a specific directory), so temporary files can be written.
                          #You can pass the actual directory in the command above by adding the parameter $TMPDIRECTORY .
    #   allowanonymous=False,
    #),
    #Action(id='multiply',name='Multiply',parameters=[
    #    IntegerParameter(id='x',name='Value'),
    #    IntegerParameter(id='y',name='Multiplier')
    #   ],
    #   function=lambda x,y: x*y
    #   allowanonymous=False,
    #),
    #Action(id="tabler",
    #       name="Tabler",
    #       allowanonymous=True,     #allow unauthenticated access to this action
    #       description="Puts a comma separated list in a table (viewer example)",
    #       function=lambda x: x,       #as you see, this function doesn't really do anything, we just demonstrate the viewer
    #       parameters=[
    #          TextParameter(id="text", name="Text", required=True),
    #       ],
    #       viewer=SimpleTableViewer(id="simpletableviewer",delimiter=",")
    # )
]

# ======= FORWARDERS =============

#Global forwarders call a remote service, passing a backlink for the remote service to download an archive of ALL the output data. The remote service is expected to return a redirect (HTTP 302) . CLAM will insert the backlink where you put $BACKLINK in the url:

#FORWARDERS = [
    #Forwarder(id='otherservice', name="Other service", description="", url="https://my.service.com/grabfrom=$BACKLINK")
#]

# ======== DISPATCHING (ADVANCED! YOU CAN SAFELY SKIP THIS!) ========

#The dispatcher to use (defaults to clamdispatcher.py), you almost never want to change this
#DISPATCHER = 'clamdispatcher.py'

#DISPATCHER_POLLINTERVAL = 30   #interval at which the dispatcher polls for resource consumption (default: 30 secs)
#DISPATCHER_MAXRESMEM = 0    #maximum consumption of resident memory (in megabytes), processes that exceed this will be automatically aborted. (0 = unlimited, default)
#DISPATCHER_MAXTIME = 0      #maximum number of seconds a process may run, it will be aborted if this duration is exceeded.   (0=unlimited, default)
#DISPATCHER_PYTHONPATH = []        #list of extra directories to add to the python path prior to launch of dispatcher

#Run background process on a remote host? Then set the following (leave the lambda in):
#REMOTEHOST = lambda: return 'some.remote.host'
#REMOTEUSER = 'username'

#For this to work, the user under which CLAM runs must have (passwordless) ssh access (use ssh keys) to the remote host using the specified username (ssh REMOTEUSER@REMOTEHOST)
#Moreover, both systems must have access to the same filesystem (ROOT) under the same mountpoint.
