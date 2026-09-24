#! /usr/bin/python

import os
import sys
import datetime
import time
import platform
import pathlib
import traceback

from LIB_STRT_Exceptions import MyLibraryException, MyCatchAllException
from LIB_STRT_Runtime import Runtime

from LIB_STRT_Logging import Logger

# ***********************************************************************************************
# ***                                                                                         ***
# *** STARTUP Library  - Perform A Standard Script StartUp Procedure                          ***
# *** ===============    -------------------------------------------                          ***
# ***********************************************************************************************
class StartUp:

  def LogMsg(self, pMsg):
    self.INT_MyLoggingObj.LogMsg(pMsg)

  def INT_Task_SetGroup(self, pTaskGroupID:int, pTaskMessage:str):
    self.INT_TaskGroupID = pTaskGroupID
    self.INT_TaskMsg = pTaskMessage

    print ('.  ' + self.INT_TaskMsg + ' .....')

  def INT_Task_ThrowError(self, pFatalError: bool, pErrorCode:int, pErrorMsg:str, pErrorSolution:str):
    MyLibraryException(pFatalError, self.INT_LibraryId, self.INT_LibraryName, \
                       self.INT_TaskGroupID, pErrorCode, \
                       self.INT_TaskMsg, pErrorMsg, pErrorSolution)

  def INT_TaskThrowUntrapped(self, pErrorCode:int, pErrorMsg:str, pMyException:Exception):
    self.INT_Task_ThrowError(True, pErrorCode, pErrorMsg, 'CODE ERROR : Check Python Exception Report')
    raise MyCatchAllException(pMyException)
    #MyCatchAllException(pMyException)

  def INT_InitRuntimeValues(self):

    # -- Get System Time UTC
    try:
      self.INT_RuntimeValues['SYSTEM-STARTTIMEUTC'] = datetime.datetime.now().timestamp()
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(1, \
                                  'Unable To Get System UTC DateTime', \
                                  MyException)

    try:
      locPath = pathlib.Path(__file__)
      self.INT_RuntimeValues['SYSTEM-PROGRAMNAME'] = locPath.name
      self.INT_RuntimeValues['SYSTEM-PROGRAMPATH'] = locPath.parent
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(2, \
                                  'Unable To Get Path Components From ScriptName', \
                                  MyException)

    try:
      self.INT_RuntimeValues['SYSTEM-HOSTNAME'] = platform.node()
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(3, \
                                  'Unable To Get Hostname', \
                                  MyException)

    try:
      self.INT_RuntimeValues['SYSTEM-LOGINNAME'] = os.getlogin()
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(4, \
                                  'Unable To Get Hostname', \
                                  MyException)

    try:
      self.INT_RuntimeValues['SYSTEM-RUNUSER'] = os.environ.get('USER')
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(5, \
                                  'Unable To Get Hostname', \
                                  MyException)

    try:
      self.INT_RuntimeValues['SYSTEM-SCRIPTPARAMETERS'] = sys.argv[1:]
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(6, \
                                  'Unable To Get Hostname', \
                                  MyException)

    try:
      self.INT_RuntimeValues['SYSTEM-PID'] = os.getpid()
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(6, \
                                  'Unable To Get Process Id', \
                                  MyException)


  def __init__(self):

    self.INT_LibraryId: int   = 1
    self.INT_LibraryName: str = 'StartUp'

    print('******************************************************************************************************')
    print('***                                                                                                ***')
    print('***             Crown Agents Bank - Unix Scripting - Standard Script StartUP                       ***')
    print('***             ============================================================                       ***')
    print('***                                                                                                ***')
    print('******************************************************************************************************')
    print('. Standard Startup (Screen Output ONLY!) .....')

    # ==========================================================================================
    # === Declare ALL Variables HERE!                                                        ===
    # ==========================================================================================
    self.INT_RuntimeValues = dict()
    self.INT_RuntimeStatus = dict()

    self.INT_RuntimeStatus['ROOT'] = 'NOT-STARTED'
    self.INT_RuntimeStatus['RUNTIME-ENV'] = 'NOT-STARTED'
    self.INT_RuntimeStatus['LOGGING'] = 'NOT-STARTED'

    # ==========================================================================================
    # === Get Scripts ROOT Location From Environment                                         ===
    # ==========================================================================================
    self.INT_Task_SetGroup(1, 'Get Scripts ROOT Location From Environment')

    try:
      self.INT_RuntimeValues['SYSTEM-ROOT'] = os.environ['MIKE_ROOT']
      self.INT_RuntimeStatus['ROOT'] = 'COMPLETED'
    except KeyError:
      self.INT_Task_ThrowError(True, 1, \
                               'Cannot Get Environment Variable [MIKE_ROOT]\nEnvironment Variable NOT DEFINED\nIn Your Shell Run [env | grep MIKE_ROOT]\n' + \
                               'This Should Return A Directory Location That Points\nTo The ROOT Location For All Scripts', \
                               'Ensure Your .profile Exports MIKE_ROOT Which Should Be the Directory That Contains The Location\n' + \
                               'Of The ROOT Directory Pointing To All Scripts OR Manually Export To Test')
      sys.exit(1)
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(True, 1, \
                                  'Cannot Get Environment Variable [MIKE_ROOT]', \
                                  MyException)
      sys.exit(1)
    else:
      print('.   .SCRIPT ROOT : ' + str(self.INT_RuntimeValues['SYSTEM-ROOT']) )

    print('.')

    # ==========================================================================================
    # === Gather ALL System Information Here                                                 ===
    # ==========================================================================================
    self.INT_Task_SetGroup(2, 'Gather ALL System And Process Information')
    try:
      self.MyRuntime = Runtime(sys.argv[0])
      self.INT_RuntimeValues['SYSTEM-STARTTIMEUTC'] = self.MyRuntime.INT_STARTTIMEUTC
      self.INT_RuntimeValues['SYSTEM-PROGRAMNAME'] = self.MyRuntime.INT_PROGRAMNAME
      self.INT_RuntimeValues['SYSTEM-PROGRAMPATH'] = self.MyRuntime.INT_PROGRAMPATH
      self.INT_RuntimeValues['SYSTEM-HOSTNAME'] = self.MyRuntime.INT_HOSTNAME
      self.INT_RuntimeValues['SYSTEM-LOGINNAME'] = self.MyRuntime.INT_LOGINNAME
      self.INT_RuntimeValues['SYSTEM-RUNUSER'] = self.MyRuntime.INT_RUNUSER
      self.INT_RuntimeValues['SYSTEM-SCRIPTPARAMETERS'] = self.MyRuntime.INT_SCRIPTPARAMETERS
      self.INT_RuntimeValues['SYSTEM-PID'] = self.MyRuntime.INT_SYSTEMPID
      self.INT_RuntimeValues['SYSTEM-STARTTIMESTR']  = datetime.datetime.fromtimestamp(self.MyRuntime.INT_STARTTIMEUTC).strftime('%Y-%m-%d.%H-%M-%S')
      self.INT_RuntimeValues['SYSTEM-STARTTIMEDATE']  = datetime.datetime.fromtimestamp(self.MyRuntime.INT_STARTTIMEUTC).strftime('%A %d %B %Y')
      self.INT_RuntimeValues['SYSTEM-STARTTIMETIME']  = datetime.datetime.fromtimestamp(self.MyRuntime.INT_STARTTIMEUTC).strftime('%I:%M.%S %p')


      self.INT_RuntimeStatus['RUNTIME-ENV'] = 'COMPLETED'
    except MyCatchAllException as MyException:
      self.INT_Task_ThrowError(True, 1, \
                               'Cannot Get Runtime Information From System', \
                               'Probably A Programming Error')
      sys.exit(1)
    else:
      print('.   ...START UTC : ' + str(self.INT_RuntimeValues['SYSTEM-STARTTIMEUTC']) )
      print('.   ..START TIME : ' + str(self.INT_RuntimeValues['SYSTEM-STARTTIMESTR']) )
      print('.   .SCRIPT ROOT : ' + str(self.INT_RuntimeValues['SYSTEM-ROOT']) )
      print('.   .....PROGRAM : ' + str(self.INT_RuntimeValues['SYSTEM-PROGRAMNAME']) )
      print('.   ....BASENAME : ' + str(self.INT_RuntimeValues['SYSTEM-PROGRAMPATH']) )
      print('.   ....HOSTNAME : ' + str(self.INT_RuntimeValues['SYSTEM-HOSTNAME']) )
      print('.   .......LOGIN : ' + str(self.INT_RuntimeValues['SYSTEM-LOGINNAME']) )
      print('.   ....USERNAME : ' + str(self.INT_RuntimeValues['SYSTEM-RUNUSER']) )
      print('.   ...PARAMETER : ' + str(self.INT_RuntimeValues['SYSTEM-SCRIPTPARAMETERS']) )
      print('.   .........PID : ' + str(self.INT_RuntimeValues['SYSTEM-PID']) )
      print('.')

    # ==========================================================================================
    # === Update The Alert Log File                                                          ===
    # ==========================================================================================

    # ==========================================================================================
    # === Update the JOBS Database                                                           ===
    # ==========================================================================================

    # ==========================================================================================
    # === Open A Log File And Print Out A Standard Job Header                                ===
    # ==========================================================================================
    self.INT_Task_SetGroup(3, 'Start Script Logging')

    self.INT_RuntimeValues['LOGGING-BASE'] = str(self.INT_RuntimeValues['SYSTEM-ROOT']) + '/logs'
    try:
      self.INT_MyLoggingObj = Logger( self.INT_RuntimeValues['LOGGING-BASE'], self.INT_RuntimeValues['SYSTEM-STARTTIMEUTC'], self.INT_RuntimeValues['SYSTEM-PROGRAMNAME'], self.INT_RuntimeValues['SYSTEM-PID'] )
    except MyLibraryException as MyException:
      self.INT_TaskThrowUntrapped(1, \
                                  'Error Calling Logging Library', \
                                  MyException)
      sys.exit(1)
    except MyCatchAllException as MyException:
      pass
    else:
      self.INT_RuntimeValues['LOGGING-DIRECTORY'] = self.INT_MyLoggingObj.INT_DirectoryPath
      self.INT_RuntimeValues['LOGGING-FILENAME'] = self.INT_MyLoggingObj.INT_FileName
      self.INT_RuntimeValues['LOGGING-FILEWITHPATH'] = self.INT_MyLoggingObj.INT_FileWithPath

      print('.   ........BASE : ' + str(self.INT_RuntimeValues['LOGGING-BASE']) )
      print('.   ...DIRECTORY : ' + str(self.INT_RuntimeValues['LOGGING-DIRECTORY']) )
      print('.   ....FILENAME : ' + str(self.INT_RuntimeValues['LOGGING-FILENAME']) )
      print('.   ...FULL PATH : ' + str(self.INT_RuntimeValues['LOGGING-FILEWITHPATH']) )
      print('.')

      try:
        self.INT_MyLoggingObj.OpenLogfile()
      except MyLibraryException as MyException:
        self.INT_TaskThrowUntrapped(1, \
                                    'Error Calling Logging Library', \
                                    MyException)
        sys.exit(1)
      except MyCatchAllException as MyException:
        pass
      else:
        if self.INT_MyLoggingObj.INT_FileOpened == True:
          self.INT_RuntimeValues['LOGGING-FILESTATUS'] = 'OPENED'
          print('.   Log File Opened For Write.')
        else:
          self.INT_RuntimeValues['LOGGING-FILESTATUS'] = 'FAILED'
          print('.   FAILED To Open Log File For Write.')
          sys.exit(1)

    # ==========================================================================================
    # === We Can Now Log To A File And To Screen                                             ===
    # ==========================================================================================
      print('.')
      print('. --------------------------------------------------------------------')
      print('. Standard Startup - Completed !, Logging to Screen And File Now .....')
      print('. --------------------------------------------------------------------')
      print('.')

      self.INT_MyLoggingObj.LogMsg('┌────────────────┬───────────────────────────────────────────────────────────────────────────────────┐')
      self.INT_MyLoggingObj.LogMsg('│                │                                                                                   │')
      self.INT_MyLoggingObj.LogMsg('│        Program │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['SYSTEM-PROGRAMNAME']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│                │                                                                                   │')
      self.INT_MyLoggingObj.LogMsg('│       Location │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['SYSTEM-PROGRAMPATH']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│     Parameters │ ' + '{0: <81}'.format(str(self.INT_RuntimeValues['SYSTEM-SCRIPTPARAMETERS']) ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│        Started │ ' + '{0: <81}'.format(str(self.INT_RuntimeValues['SYSTEM-STARTTIMEDATE']) + ' @ ' + str(self.INT_RuntimeValues['SYSTEM-STARTTIMETIME']) ) + ' │')
      self.INT_MyLoggingObj.LogMsg('├────────────────┼───────────────────────────────────────────────────────────────────────────────────┤')
      self.INT_MyLoggingObj.LogMsg('│            PID │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['SYSTEM-PID']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│      Host Name │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['SYSTEM-HOSTNAME']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│     Login Name │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['SYSTEM-LOGINNAME']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│  Run User Name │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['SYSTEM-RUNUSER']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('├────────────────┼───────────────────────────────────────────────────────────────────────────────────┤')
      self.INT_MyLoggingObj.LogMsg('│   Scripts ROOT │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['SYSTEM-ROOT']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│       Log Base │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['LOGGING-BASE']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│  Log Directory │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['LOGGING-DIRECTORY']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('│  Log File Name │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['LOGGING-FILENAME']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('└────────────────┴───────────────────────────────────────────────────────────────────────────────────┘')

      self.INT_RuntimeValues['SYSTEM-STARTTIMEDATE']  = datetime.datetime.fromtimestamp(self.MyRuntime.INT_STARTTIMEUTC).strftime('%Y-%m-%d')
      self.INT_RuntimeValues['SYSTEM-STARTTIMETIME']  = datetime.datetime.fromtimestamp(self.MyRuntime.INT_STARTTIMEUTC).strftime('%H-%M-%S')

      # Handback Control to the calling program......

  def Terminate(self):
      self.INT_MyLoggingObj.LogMsg('┌────────────────┬───────────────────────────────────────────────────────────────────────────────────┐')
      self.INT_MyLoggingObj.LogMsg('│        Program │ ' + '{0: <81}'.format('[' + str(self.INT_RuntimeValues['SYSTEM-PROGRAMNAME']) + ']' ) + ' │')
      self.INT_MyLoggingObj.LogMsg('├────────────────┼───────────────────────────────────────────────────────────────────────────────────┤')
      self.INT_MyLoggingObj.LogMsg('│                │                  COMPLETED !!                                                     │')
      self.INT_MyLoggingObj.LogMsg('└────────────────┴───────────────────────────────────────────────────────────────────────────────────┘')

      self.INT_MyLoggingObj.CloseLogfile()

      sys.exit()

