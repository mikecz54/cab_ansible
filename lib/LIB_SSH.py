import time
import subprocess

class SSHFailedToConnect(Exception):
  def __init__(self):
    self.message = 'Unable to Connect To Remote Host'
    super().__init__()

class SSHBadCommand(Exception):
  def __init__(self):
    self.message = 'Bad Command In SSH'
    super().__init__()

class SSHProgramFailed(Exception):
  def __init__(self):
    self.message = 'Called Program Returned Failure'
    super().__init__()

class MySSH():

  def __init__(self, pHostName):

    self.SSH_Hostname = pHostName

  def RunCommand(self, pCommand):

    MySubprocess = subprocess.run(['ssh', '-q', self.SSH_Hostname, pCommand], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if  MySubprocess.returncode == 255:
      raise SSHFailedToConnect()
    if  MySubprocess.returncode == 127:
      raise SSHBadCommand()
    if  MySubprocess.returncode == 1:
      SSHProgramFailed()
    else:
      MyReturn = []
      for line in filter(None, MySubprocess.stdout.split('\n')):
        MyReturn.append(line)
      return MyReturn


# THIS CLASS WILL BE CALLED BY THE DNF CLASS NOT BY THE SCRIPT DIRECTLY !!!!!
    # call os run process
#   print('=============================================================================================')
#   print('CALLING SSH')
#   print('=============================================================================================')
#   MySubprocess = subprocess.run(['ssh', '-q', self.SSH_Hostname, pCommand], text=True, stdout=subprocess.PIPE)

#   print('---------------------------------------------------------------------------------------------')
#   print('RETURN : ' + str(MySubprocess.returncode) )
#   print('OUTPUT : ')
#   for line in filter(None, MySubprocess.stdout.split('\n')):
#     print('       > ' + str(line))

#   print('---------------------------------------------------------------------------------------------')

#   print(' ERROR : ')
#   for line in filter(None, MySubprocess.stderr.split('\n')):
#     print('       > ' + str(line))

#   print('---------------------------------------------------------------------------------------------')

