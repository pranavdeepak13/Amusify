import streamlit as st
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import os
import base64
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

def get_token(clientId,clientSecret):
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}
    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')
    headers['Authorization'] = "Basic " + base64Message
    data['grant_type'] = "client_credentials"
    r = requests.post(url, headers=headers, data=data)
    token = r.json()['access_token']
    return token

def get_track_recommendations(seed_tracks,token):
    limit = 10
    recUrl = f"https://api.spotify.com/v1/recommendations?limit={limit}&seed_tracks={seed_tracks}"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=recUrl, headers=headers)
    return res.json()

def song_recommendation_vis(df):
    df['duration_min'] = round(df['duration_ms']/1000,0)
    df['popularity_range'] = df['popularity']-(df['popularity'].min()-1)
    plt.figure(figsize=(15,6),facecolor='white')
    x = df['name']
    y = df['duration_min']
    s = df['popularity_range']*20

    color_lables = df['explicit'].unique()
    rgb_values = sns.color_palette("Set1",8)
    color_map = dict(zip(color_lables,rgb_values))
    plt.scatter(x,y,s,alpha=0.7,c=df['explicit'].map(color_map))
    plt.xlabel("Song Name")
    plt.ylabel("Duration (ms)")
    plt.xticks(rotation=90)
    plt.legend()
    plt.title("Song Recommendations")
    st.pyplot(plt)

def save_album_image(img_url, track_id):
    r = requests.get(img_url)
    open('img/' + track_id + '.jpg', "wb").write(r.content)
    
def get_album_mage(track_id):
    return Image.open('img/' + track_id + '.jpg')