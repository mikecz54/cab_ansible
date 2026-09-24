#!/bin/python

import dnf
import hawkey


MyDNFObject = dnf.Base()
MyDNFObject.fill_sack()

MyPackagesObject = MyDNFObject.sack.query()


# ====================================================================================================
# === Gather All Packages Installed                                                                ===
# ====================================================================================================
#MyPackagesInstalled = MyPackagesObject.installed()
#OutPackages = list(MyPackagesInstalled)
#
#for OutPkgLine in OutPackages:
#  print('Package : ' + str(OutPkgLine) )
#  Package : NessusAgent-10.7.3-el9.x86_64
#
#  print("name: {}".format(OutPkgLine.name) )
#  print("version: {}".format(OutPkgLine.version) )
#  print("release: {}".format(OutPkgLine.release) )
#  print("arch: {}".format(OutPkgLine.arch) )
#
#  print("epoch: {}".format(OutPkgLine.epoch) )
#  print("summary: {}".format(OutPkgLine.summary) )
#
#  print("{0:50s} : {1:10s} : {2:15s} : {3:10s}".format(OutPkgLine.name, OutPkgLine.version, OutPkgLine.release, OutPkgLine.arch) )

# ====================================================================================================
# === Gather All Packages That Can Be Upgraded                                                     ===
# ====================================================================================================
#MyPackagesUpgradable = MyPackagesObject.upgrades()
#UpgPackages = list(MyPackagesUpgradable)
#
#for UpgPkgLine in UpgPackages:
#
#  print('Package : ' + str(UpgPkgLine) )

# ====================================================================================================
# === Get Repository Information                                                                   ===
# ====================================================================================================
MyRepositoryObject = MyDNFObject.read_all_repos()

MyReposAll = MyRepositoryObject.all()

for OutUpgrdPkg in list(MyRepositoryObject) :
  print('Repo : ' + str(OutUpgrdPkg) )
