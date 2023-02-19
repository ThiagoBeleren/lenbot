import os

def Token():
  return os.environ['TOKEN']


def SpotifyClientID():
  return os.environ['spotifyClientId']


def SpotifyClientSecret():
  return os.getenv['spotifyClientSecret']
