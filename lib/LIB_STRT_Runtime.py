#! /usr/bin/python

import os
import sys
import datetime
import time
import platform
import pathlib

from LIB_STRT_Exceptions import MyLibraryException, MyCatchAllException

# ***********************************************************************************************
# ***                                                                                         ***
# *** RUNTIME Library  - Gather All System And Process Information                            ***
# *** ===============    -----------------------------------------                            ***
# ***********************************************************************************************
class Runtime:

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
    MyCatchAllException(pMyException)

  def __init__(self, pScriptName:str):

    self.INT_LibraryId: int   = 2
    self.INT_LibraryName: str = 'Runtime'

    # ==========================================================================================
    # === Get ALL Runtime Information                                                        ===
    # ==========================================================================================
    self.INT_Task_SetGroup(1, 'Get Runtime Environment')

    # -- ---------------------------------------------------------------------------------------
    # -- Get System Time UTC                                                                 ---
    # -- ---------------------------------------------------------------------------------------
    try:
      self.INT_STARTTIMEUTC = datetime.datetime.now().timestamp()
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(1, \
                                  'Unable To Get System UTC DateTime', \
                                  MyException)

    # -- ---------------------------------------------------------------------------------------
    # -- Get Program Information                                                             ---
    # -- ---------------------------------------------------------------------------------------
    try:
      locPath = pathlib.Path(pScriptName)
      self.INT_PROGRAMNAME = locPath.name
      self.INT_PROGRAMPATH = locPath.parent
      self.INT_PROGRAMNAME = os.path.basename(pScriptName)
      self.INT_PROGRAMPATH = os.path.dirname(os.path.abspath(pScriptName))
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(2, \
                                  'Unable To Get Path Components From ScriptName', \
                                  MyException)

    # -- ---------------------------------------------------------------------------------------
    # -- Get Hostname                                                                        ---
    # -- ---------------------------------------------------------------------------------------
    try:
      self.INT_HOSTNAME = platform.node()
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(3, \
                                  'Unable To Get Hostname', \
                                  MyException)

    # -- ---------------------------------------------------------------------------------------
    # -- Get Login Name                                                                      ---
    # -- ---------------------------------------------------------------------------------------
    try:
      self.INT_LOGINNAME = os.getlogin()
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(4, \
                                  'Unable To Get Hostname', \
                                  MyException)

    # -- ---------------------------------------------------------------------------------------
    # -- Get Run User Name                                                                   ---
    # -- ---------------------------------------------------------------------------------------
    try:
      self.INT_RUNUSER = os.environ.get('USER')
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(5, \
                                  'Unable To Get Hostname', \
                                  MyException)

    # -- ---------------------------------------------------------------------------------------
    # -- Get Script Parameters                                                               ---
    # -- ---------------------------------------------------------------------------------------
    try:
      self.INT_SCRIPTPARAMETERS = sys.argv[1:]
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(6, \
                                  'Unable To Get Hostname', \
                                  MyException)

    # -- ---------------------------------------------------------------------------------------
    # -- Get Process PID                                                                     ---
    # -- ---------------------------------------------------------------------------------------
    try:
      self.INT_SYSTEMPID = os.getpid()
    except Exception as MyException:
      self.INT_TaskThrowUntrapped(6, \
                                  'Unable To Get Process Id', \
                                  MyException)


