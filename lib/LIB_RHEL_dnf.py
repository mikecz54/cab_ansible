
import os
import sys
import datetime
import time

from LIB_SSH import MySSH, SSHFailedToConnect, SSHBadCommand, SSHProgramFailed

# Exception classes here


class DNFFailedStartUp(Exception):
  def __init__(self):
    self.message = 'HOST Failed To Start'
    super().__init__()

class DNFFailedShutdown(Exception):
  def __init__(self):
    self.message = 'HOST Failed To Shutdown'
    super().__init__()

class RHEL_DNF_Updater():

  def CreateTodaysDirectory(self):
    TMP_DateTime = datetime.datetime.fromtimestamp(self.StartTimeUTC).strftime('%Y-%m-%d')
    TMP_NewPath = self.INT_DirectoryBase + '/' + TMP_DateTime

    try:
      os.makedirs(TMP_NewPath, exist_ok=True)
    except:
      self.INT_Task_ThrowError(True, 1, \
                             'Unable to Create Todays Date Directory',
                             'Check The error')
    else:
      self.INT_DirectoryPath = TMP_NewPath

  def GenerateReport(self):

    self.ReportFilename = 'dnfupdate.' + self.DNFHostname + '.txt'
    self.CreateTodaysDirectory()
    self.MyDNFReport = self.INT_DirectoryPath + '/' + self.ReportFilename


    with open(self.MyDNFReport, 'w') as MySummaryReport:
       MySummaryReport.write('SUMMARY REPORT FOR ' + self.DNFHostname +'\n')
       MySummaryReport.write('\n')
       for line in self.MyUpdateResults:
         MySummaryReport.write(line + '\n')

       MySummaryReport.write('\n')
       if self.MyRebootRequested:
         MySummaryReport.write('SERVER REBOOT REQUESTED\n\n')
         MySummaryReport.write('\n')
         if self.MySHUTDOWN_COMPLETED:
           MySummaryReport.write('Server Shutdown was successful\n')
         else:
           MySummaryReport.write('Server Shutdown failed\n')
         if self.MySTARTUP_COMPLETED:
           MySummaryReport.write('Server Startup was successful\n')
           MySummaryReport.write('Server Uptime : ' + str(self.MyRebootResult))
         else:
           MySummaryReport.write('Server Startup failed\n\n')

       MySummaryReport.write('***** END OF REPORT *****\n')

    MySummaryReport.close()


  def __init__(self, pSTARTUTC,  pHostName, pReportRoot):

    self.INT_DirectoryBase = '/home/cab_ansible/CAB_ADMIN/reports/osupdates'

    self.DNFHostname = pHostName
    self.ReportROOT = pReportRoot
    self.StartTimeUTC = pSTARTUTC

    self.MyRebootRequested = False
    self.MySHUTDOWN_COMPLETED = False
    self.MySTARTUP_COMPLETED = False
    self.MyRebootResult = None

    try:
      self.MySHObject = MySSH(pHostName)
      MySSH_ConnectionGood = self.MySHObject.RunCommand('hostname')
    except SSHFailedToConnect as MyException:
      raise SSHFailedToConnect()
    except SSHBadCommand as MyException:
      raise SSHBadCommand()
    except SSHProgramFailed as MyException:
      raise SSHProgramFailed()
    else:
      for line in MySSH_ConnectionGood:
        print('       > ' + str(line))

  def DNFUpdatePackages(self):

    try:
      self.MyUpdateResults = self.MySHObject.RunCommand('sudo dnf upgrade --assumeyes')
    except SSHFailedToConnect as MyException:
      raise SSHFailedToConnect()
    except SSHBadCommand as MyException:
      raise SSHBadCommand()
    except SSHProgramFailed as MyException:
      raise SSHProgramFailed()

#  def CheckForDisconnect(self):

#  def CheckForConnect(self):


  def DNFHostREBOOT(self):

    self.MyRebootRequested = True

    try:
      self.MyRebootResult = self.MySHObject.RunCommand('sudo shutdown -r 1')
    except SSHFailedToConnect as MyException:
      raise SSHFailedToConnect()
    except SSHBadCommand as MyException:
      raise SSHBadCommand()
    except SSHProgramFailed as MyException:
      raise SSHProgramFailed()
    else:

      # NOW CHECK ITS SHUTDOWN !
      # ----------------------
      locSHUTDOWNLOOP = True
      locSHUTDOWNTRIES = 0
      while locSHUTDOWNLOOP:
        try:
          self.MyRebootResult = self.MySHObject.RunCommand('uptime')
        except:
          locSHUTDOWNLOOP = False
          self.MySHUTDOWN_COMPLETED = True
        else:
          locSHUTDOWNTRIES += 1

        # Wait 10 Minutes after that bin out and alert!!!!
        time.sleep(15)
        if locSHUTDOWNTRIES > 40 :
          locSHUTDOWNLOOP = False
          self.MySHUTDOWN_COMPLETED = False

      if self.MySHUTDOWN_COMPLETED:
        # NOW CHECK ITS BACK UP !
        # ---------------------
        locSTARTUPLOOP = True
        locSTARTUPTRIES = 0
        while locSTARTUPLOOP:
          try:
            self.MyRebootResult = self.MySHObject.RunCommand('uptime')
          except:
            locSTARTUPTRIES += 1
          else:
            locSTARTUPLOOP = False
            self.MySTARTUP_COMPLETED = True

          # Wait 10 Minutes after that bin out and alert!!!!
          time.sleep(15)
          if locSTARTUPTRIES > 40 :
            locSTARTUPLOOP = False
            self.MySTARTUP_COMPLETED = False

        if self.MySTARTUP_COMPLETED:
          pass
        else:
          raise DNFFailedStartUp()
      else:
         raise DNFFailedShutdown()

