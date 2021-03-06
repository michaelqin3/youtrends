from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import os
from flask import jsonify
from app import models, db
import re
import random

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY = os.getenv('API_DEVELOPER_KEY')
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

countries = ['RU', 'CA', 'US', 'JP', 'MX', 'KR', 'IN']


def getChannelTitleById(id):
    response = youtube.channels().list(part='snippet', id=id).execute()
    return response['items'][0]['snippet']['title']


def getVideos():
    response = youtube.videos().list(part='snippet,id,statistics',
                                     chart='mostPopular').execute()
    videos = []
    resultsLeft = response['pageInfo']['totalResults']
    resultsPerPage = response['pageInfo']['resultsPerPage']
    while True:
        videos = videos + [
            models.Video(id=v['id'], title=cleanTitle(v['snippet']['title']), category_id=v['snippet']['categoryId'],
                         thumbnail=v['snippet']['thumbnails']['high']['url'],
                         channel_id=v['snippet']['channelId'], publish_time=(
                             v['snippet']['publishedAt']).split('T')[0],
                         views=v['statistics']['viewCount'], likes=v['statistics']['likeCount'] if 'likeCount' in v['statistics'] else 0,
                         trending_country=random.choice(countries),
                         dislikes=v['statistics']['dislikeCount'] if 'dislikeCount' in v['statistics'] else 0) for v in response['items'] if nonDuplicateVid(v['id'])
        ]
        resultsLeft -= resultsPerPage
        if (resultsLeft > resultsPerPage):
            nextPageToken = response['nextPageToken']

            response = youtube.videos().list(part='snippet,id,statistics',
                                             chart='mostPopular', pageToken=nextPageToken).execute()
        else:
            break
    db.session.bulk_save_objects(videos)
    db.session.commit()


def nonDuplicateVid(id):
    return models.Video.query.get(id) is None


def cleanTitle(title):
    return re.sub('[^A-Za-z0-9\s]+', '', title)
