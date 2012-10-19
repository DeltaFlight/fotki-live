#!/usr/bin/python

import pygame
import pygame.image
import pygame.display
import pygame.event
import pygame.transform
import time
import sys
import urllib2
from xml.dom import minidom
import socket

TMP = "/tmp/image.jpg"
SLEEP_SECONDS = 2

def update():
  src = urllib2.urlopen("http://fotki.yandex.ru/live/rss2")
  dom = minidom.parse(src)
  return dom.getElementsByTagName("item")


def download(item):
  urlEl = item.getElementsByTagName("media:content")[0]
  url = urlEl.attributes["url"].value
  url = url.replace("_XL", "_XXXL")
  image = urllib2.urlopen(url)
  out = open(TMP, "wb")
  out.write(image.read())
  out.close()

def display():
  picture = pygame.image.load(TMP)
  (width, height) = picture.get_size()
  ratioH = float(screen_height) / height
  ratioV = float(screen_width) / width
  ratio = min(ratioH, ratioV)
  newsize = (int(width * ratio), int(height* ratio))
  if picture.get_bitsize() < 24:
    picture = pygame.transform.scale(picture, newsize)
  else:
    picture = pygame.transform.smoothscale(picture, newsize)
  dx = (screen_width - picture.get_width()) / 2
  dy = (screen_height - picture.get_height()) / 2
 
  buf = surface.copy() 
  buf.fill(0)
  buf.blit(picture, (dx, dy))
  surface.blit(buf, (0, 0))
  pygame.display.flip()

def maybeExit():
  for i in xrange(0, SLEEP_SECONDS * 2):
    if pygame.event.peek(pygame.KEYDOWN):
      event = pygame.event.get(pygame.KEYDOWN)[0]
      print event
      if event.key == 27:
        sys.exit(0)
    pygame.event.get()
    time.sleep(0.5)

surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

while True:
  try:
    items = update()
    for item in items:
      download(item)
      display()
      maybeExit()
  except urllib2.HTTPError, ex:
    print ex
    time.sleep(1)
  except socket.error, ex:
    print ex
    time.sleep(1)

