#!/usr/bin/python

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# with open('dev_key') as f :
#     key=f.readline().strip()
# #print key
# DEVELOPER_KEY = key
# print DEVELOPER_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY=""

def youtube_search(movie,DEVELOPER_KEY):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=movie+" trailer",
    part='id,snippet',
    maxResults=1
  ).execute()

  videos = []
  ids=[]

  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s (%s)' % (search_result['snippet']['title'],
                                 search_result['id']['videoId']))
      ids.append(str(search_result['id']['videoId']))
  stx=""

  for x in ids :
    stx=stx+x+","
  #print stx
  return stx[:-1]


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='Submarine 2010')
  parser.add_argument('--max-results', help='Max results', default=1)
  args = parser.parse_args()

  try:
    youtube_search(args,DEVELOPER_KEY)
    #print args
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
