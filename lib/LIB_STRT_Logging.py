import os
import sys
import datetime

from LIB_STRT_Exceptions import MyLibraryException, MyCatchAllException

class Logger():

  def INT_Task_SetGroup(self, pTaskGroupID:int, pTaskMessage:str):
    self.INT_TaskGroupID = pTaskGroupID
    self.INT_TaskMsg = pTaskMessage

    print ('.  ' + self.INT_TaskMsg + ' .....')

  def INT_Task_ThrowError(self, pFatalError: bool, pErrorCode:int, pErrorMsg:str, pErrorSolution:str):
    raise MyLibraryException(pFatalError, self.INT_LibraryId, self.INT_LibraryName, \
                       self.INT_TaskGroupID, pErrorCode, \
                       self.INT_TaskMsg, pErrorMsg, pErrorSolution)

  def INT_TaskThrowUntrapped(self, pErrorCode:int, pErrorMsg:str, pMyException:Exception):
    self.INT_Task_ThrowError(True, pErrorCode, pErrorMsg, 'CODE ERROR : Check Python Exception Report')
    raise MyCatchAllException(pMyException)

  def INIT_Checks(self, pDirectoryPath):

    if os.path.isdir(pDirectoryPath):
      if os.access(pDirectoryPath, os.W_OK):
        self.INT_DirectoryBase = pDirectoryPath
      else:
        self.INT_Task_ThrowError(True, 1, \
                               'The logs directory Is NOT Writable so we cannot log to a file',
                               'Please Change the logs directory to be writable by this user.')
    else:
      self.INT_Task_ThrowError(True, 1, \
                             'The logs directory does NOT exist so we cannot log to a file',
                             'Please create the logs director under The Scripts ROOT Directory')

  def CreateTodaysDirectory(self, pSTARTUTC):
    TMP_DateTime = datetime.datetime.fromtimestamp(pSTARTUTC).strftime('%Y-%m-%d')
    TMP_NewPath = self.INT_DirectoryBase + '/' + TMP_DateTime

    try:
      os.makedirs(TMP_NewPath, exist_ok=True)
    except:
      self.INT_Task_ThrowError(True, 1, \
                             'Unable to Create Todays Date Directory',
                             'Check The error')
    else:
      self.INT_DirectoryPath = TMP_NewPath

  def OpenLogfile(self):
    # Open File now.
    if self.INT_FileOpened :
      print('You Can Only Open The Logfile Once!')
    else:
      self.INT_MYLogfileFile_Obj = open(self.INT_FileWithPath, 'w')
      self.INT_FileOpened = True

  def CloseLogfile(self):
    if self.INT_FileOpened :
      self.INT_MYLogfileFile_Obj.close()
    else:
      print('You Have Not Opened The Logfile So I Cant Close It!')


  def LogMsg(self, pMessage):

    if self.INT_FileOpened :
      self.INT_MYLogfileFile_Obj.write(pMessage + '\n')

    print(pMessage)

  def __init__(self, pDIRECTORY:str, pSTARTUTC, pPROGRAMNAME:str, pPID):
    self.INT_LibraryId: int   = 3
    self.INT_LibraryName: str = 'Logger'

    self.INT_FileOpened = False
    TMP_DateTime = datetime.datetime.fromtimestamp(pSTARTUTC).strftime('%Y-%m-%d.%H-%M-%S')

    self.INT_BaseName = pPROGRAMNAME
    self.INT_DateTime = TMP_DateTime
    self.INT_PID      = pPID

    # ==========================================================================================
    # === Check LOG Directory Exists And Is Writable                                         ===
    # ==========================================================================================
    self.INT_Task_SetGroup(1, 'Check Log Directory')

    try:
      self.INIT_Checks(pDIRECTORY)
    except MyLibraryException as MyException:
      self.INT_Task_ThrowError(True, 1, \
                             'Error Performing LOG DIRECTORY Checks',
                             'Check you Config')

    # ==========================================================================================
    # === Create Todays Date Directory For This Log File                                     ===
    # ==========================================================================================
    self.INT_Task_SetGroup(2, 'Create Todays Date Logging Directory')
    self.CreateTodaysDirectory(pSTARTUTC)

    self.INT_FileName = str(pPROGRAMNAME) + '.' + str(TMP_DateTime) + '.' + str(self.INT_PID) + '.log'
    self.INT_FileWithPath = self.INT_DirectoryPath + '/' + self.INT_FileName
