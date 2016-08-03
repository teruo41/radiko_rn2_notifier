#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
import json
import urllib2
import subprocess
import pytz
from datetime import datetime
import time

class RadikoList:
  __metaclass__ = ABCMeta

  def __init__(self):
    self.src_url = ""
    self.provider = ""
    self.image_url = ""
    return

  def setSrcUrl(self, url):
    self.src_url = url
    return

  def getSrcUrl(self):
    return self.src_url

  def setProvider(self, provider):
    self.provider = provider
    return

  def getProvider(self):
    return self.provier

  @abstractmethod
  def procReq(self):
    pass

  def getSource(self):
    self.r = urllib2.urlopen(self.src_url)
    self.procReq()
    return

  @abstractmethod
  def procTitle(self):
    pass

  @abstractmethod
  def procImageUrl(self):
    pass

  def setTitle(self):
    self.title = self.procTitle()
    self.image_url = self.procImageUrl()
    return self.title

  def sendNotifier(self):
    mes = self.title
    notifier_title = "Now listening to %s:" % self.provider
    content_image = self.image_url
    if content_image != "":
      cmd = ["terminal-notifier",
             "-group", "Radiko-list",
             "-message", "\"%s\"" % mes,
             "-title", "\"%s\"" % notifier_title,
             "-contentImage", "\"%s\"" % content_image,
             "-appIcon", "http://radiko.jp/images/radiko-icon-circle.png"
            ]
    else:
      cmd = ["terminal-notifier",
             "-group", "Radiko-list",
             "-message", "\"%s\"" % mes,
             "-title", "\"%s\"" % notifier_title,
             "-appIcon", "http://radiko.jp/images/radiko-icon-circle.png"
            ]
    #print
    print cmd
    subprocess.call(cmd)
    return

  def run(self):
    pretitle = ""
    for i in range(600):
      #print i,
      title = self.setTitle()

      if title == None:
        print "Cannot get music title..."
      elif title != pretitle:
        self.sendNotifier()
        pretitle = title

      time.sleep(6)
    return

class RN2(RadikoList):
  def __init__(self):
    self.setSrcUrl("http://www.radionikkei.jp/rn2/json/json.php")
    self.setProvider("RN2")
    self.root = None
    self.entry = None
    return

  def setEntry(self):
    if self.root == None:
      self.getSource()

    tz_tokyo = pytz.timezone('Asia/Tokyo')
    now = datetime.now(tz_tokyo).time()
    for entry in self.root:
      #print entry['time']
      song_time = datetime.strptime(entry['time'], "%H:%M:%S").time()
      if now > song_time:
        self.entry = entry
      else:
        break
    return
    
  def procReq(self):
    if self.root == None:
      self.root = json.loads(self.r.read())
    return

  def procTitle(self):
    self.setEntry()
    title =  self.entry['title']
    artist =  self.entry['artist']
    return title + " / " + artist

  def procImageUrl(self):
    image_url = self.entry['appleartwork100']
    return image_url

if __name__ == '__main__':
  rn2 = RN2()
  rn2.run()
