#! /usr/bin/python

import traceback

# ***********************************************************************************************
# *** Class To Handle ALL Library Exceptions                                                  ***
# ***********************************************************************************************
class MyLibraryException(Exception):

  def  __init__(self, pFATAL: bool, pLibraryID: int, pLibraryName: str, pErrorGrp: int, pErrorID: int, pInfo: str, pException: str, pSolution: str):

    print('. ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐')
    print('. │                                                                                                  │')

    if pFATAL:
      print('. │                     FATAL ERROR :: TRAPPED EXCEPTION IN LIBRARY.                                 │')
    else:
      print('. │                   NON FATAL ERROR :: TRAPPED EXCEPTION IN LIBRARY.                               │')
    print('. │                                                                                                  │')
    print('. ├──────────────────────────────────────────────────────────────────────────────────────────────────┤')

    lv_LibraryMsg = '{0: <96}'.format('Library ID [' + '{:03d}'.format(pLibraryID) + '] , Library Name [' + str(pLibraryName) + ']')
    print('. │ ' + lv_LibraryMsg + ' │')

    lv_ErrorIDMsg = '{0: <96}'.format('  Error ID [' + '{:03d}'.format(pErrorGrp) + '-' + '{:03d}'.format(pErrorID) + '] - ' + str(pInfo) )
    print('. │ ' + lv_ErrorIDMsg + ' │')

    print('. ├───────────────────────────────────────  EXCEPTION  ──────────────────────────────────────────────┤')
    lv_ExceptionInfo = pException.splitlines()
    for lv_ExceptionInfoLine in lv_ExceptionInfo:
      print('. │ ' + '{0: <97}'.format(lv_ExceptionInfoLine) + '│')

    print('. ├───────────────────────────────────  POSSIBLE SOLUTIONS  ─────────────────────────────────────────┤')
    lv_SolutionInfo = pSolution.splitlines()
    for lv_SolutionInfoLine in lv_SolutionInfo:
      print('. │ ' + '{0: <97}'.format(lv_SolutionInfoLine) + '│' )

    print('. └──────────────────────────────────────────────────────────────────────────────────────────────────┘')

# ***********************************************************************************************
# *** Class To Handle ALL UNHANDLED Exceptions                                                ***
# ***********************************************************************************************
class MyCatchAllException(Exception):

  def  __init__(self, pRootException: Exception):
  # https://stackoverflow.com/questions/11414894/extract-traceback-info-from-an-exception-object
  # https://docs.python.org/3/library/traceback.html#traceback.StackSummary

    print('. ┌──┬───────────────────────────────────────────────────────────────────────────────────────────────┐')
    print('. │  │                                                                                               │')
    print('. │  │               FATAL ERROR :: UNTRAPPED PYTHON ERROR - CODING ERROR!                           │')
    print('. │  │                                                                                               │')
    print('. ├──┼───────────────────────────────────────────────────────────────────────────────────────────────┤')

    Mytb, Myfile, Myerr = traceback.format_exception(etype=type(pRootException), value=pRootException, tb=pRootException.__traceback__)

    print('. │  │  A Python Programming Error Has Occurred, Probably A Typo In The Script                       │')
    print('. │  │  Check Your Code                                                                              │')

    print('. ├──┼───────────────────────────────────  ERROR LOCATION  ──────────────────────────────────────────┤')
    lv_ExceptionFile = Myfile.splitlines()
    for lv_ExceptionFileLine in lv_ExceptionFile:
      print('. │  │' + '{0: <95}'.format(lv_ExceptionFileLine) + '│' )


    print('. ├──┼─────────────────────────────────────  ACTUAL ERROR    ────────────────────────────────────────┤')
    lv_ExceptionError = Myerr.splitlines()
    for lv_ExceptionErrorLine in lv_ExceptionError:
       print('. │  │' + '{0: <95}'.format(lv_ExceptionErrorLine) + '│' )

    print('. └──┴───────────────────────────────────────────────────────────────────────────────────────────────┘')


