#!/usr/bin/python

import pygame
import pygame.image
import pygame.display
import pygame.event
import time
import sys
import urllib2
from xml.dom import minidom

TMP = "/tmp/image.jpg"
SLEEP_SECONDS = 1

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
  surface.fill(0)
  surface.blit(picture, (0, 0))
  pygame.display.update()
  time.sleep(SLEEP_SECONDS)
  if pygame.event.peek(pygame.KEYDOWN):
    sys.exit(0)


surface = pygame.display.set_mode((0, 0))
#, pygame.FULLSCREEN)

while True:
  items = update()
  for item in items:
    download(item)
    display()
