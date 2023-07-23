import streamlit as st
import spotipy as spy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from dotenv import load_dotenv
import os
import polarplot
import recommendations
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spy.Spotify(auth_manager=auth_manager)
st.header("Welcome to Amusify")
st.subheader("A music analytics and recommendation system")
st.write("This is a music recommendation system that recommends songs based on the song you like. It uses the Spotify API to get the songs and their features.")
st.sidebar.header("User Input Features")
search_choices = ["Song","Artist","Album"]
search_selected = st.sidebar.selectbox("Search by", search_choices)
search_keyword = st.text_input(search_selected+" ( Search Keyword )")
button_clicked = st.button("Search")
selected_album=None
selected_track=None
selected_artist=None
search_results = []
tracks = []
albums = []
artists = []
if search_keyword is not None and len(search_keyword)>0:
    if search_selected == "Song":
        st.write("You searched by Song")
        tracks = sp.search(q='track:' + search_keyword, type='track',limit=30)
        tracks_list = tracks['tracks']['items']
        if(len(tracks_list)>0):
            for track in tracks_list:
                search_results.append(track['name']+ ' - By - ' + track['artists'][0]['name'])
    elif search_selected == "Artist":
        st.write("You searched by Artist")
        artists = sp.search(q='artist:' + search_keyword, type='artist',limit=30)
        artists_list = artists['artists']['items']
        if(len(artists_list)>0):
            for artist in artists_list:
                search_results.append(artist['name'])
    elif search_selected == "Album":
        st.write("You searched by Album")
        albums = sp.search(q='album:' + search_keyword, type='album',limit=30)
        albums_list = albums['albums']['items']
        if(len(albums)>0):
            for album in albums_list:
                search_results.append(album['name'] + " - By - " + album['artists'][0]['name'])

if search_selected=='Song':
    selected_track = st.selectbox("Select Track", search_results)
elif search_selected=='Album':
    selected_album = st.selectbox("Select Album", search_results)
    st.write(selected_album)
elif search_selected=='Artist':
    selected_artist = st.selectbox("Select Artist", search_results)

if selected_track is not None and len(tracks)>0:
    tracks_list = tracks['tracks']['items']
    track_id = None
    if len(tracks_list)>0:
        for track in tracks_list:
            str_temp = track['name']+ ' - By - ' + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
    selected_track_choice= None
    if track_id is not None:
        track_choices = ["Track Features", "Track Recommendations"]
        selected_track_choice = st.sidebar.selectbox("Select", track_choices)
        if selected_track_choice == "Track Features":
            track_features = sp.audio_features(track_id)
            df = pd.DataFrame(track_features,index=[0])
            df = df[['danceability','energy','speechiness','acousticness','instrumentalness','liveness','valence']]
            polarplot.feature_plot(df)
        elif selected_track_choice == "Track Recommendations":
            st.write("Track Recommendations")
            token = recommendations.get_token(client_id,client_secret)
            track_recommendations = recommendations.get_track_recommendations(track_id,token)
            tracks_list = track_recommendations['tracks']
            df = pd.DataFrame(tracks_list)
            recom_df = df[['name','duration_ms','popularity','explicit']]
            st.write(recom_df)
            recommendations.song_recommendation_vis(recom_df)
    else :
        st.write("Please select a track")

elif selected_album is not None and len(albums)>0:
    albums_list = albums['albums']['items']
    album_id = None
    album_uri = None    
    album_name = None
    if len(albums_list) > 0:
        for album in albums_list:
            str_temp = album['name'] + " - By - " + album['artists'][0]['name']
            if selected_album == str_temp:
                album_id = album['id']
                album_uri = album['uri']
                album_name = album['name']
    if album_id is not None and album_uri is not None:
        st.write("Collecting all the tracks for the album :" + album_name)
        album_tracks = sp.album_tracks(album_id)
        df_album_tracks = pd.DataFrame(album_tracks['items'])
        df_tracks_min = df_album_tracks.loc[:,['id', 'name', 'duration_ms', 'explicit', 'preview_url']]
        for idx in df_tracks_min.index:
            with st.container():
                col1, col2, col3, col4 = st.columns((4,4,1,1))
                col11, col12 = st.columns((8,2))
                col1.write(df_tracks_min['id'][idx])
                col2.write(df_tracks_min['name'][idx])
                col3.write(df_tracks_min['duration_ms'][idx])
                col4.write(df_tracks_min['explicit'][idx])   
                if df_tracks_min['preview_url'][idx] is not None:
                    col11.write(df_tracks_min['preview_url'][idx])  
                    with col12:   
                        st.audio(df_tracks_min['preview_url'][idx], format="audio/mp3")
if selected_artist is not None and len(artists) > 0:
    artists_list = artists['artists']['items']
    artist_id = None
    artist_uri = None
    selected_artist_choice = None
    if len(artists_list) > 0:
        for artist in artists_list:
            if selected_artist == artist['name']:
                artist_id = artist['id']
                artist_uri = artist['uri']
    
    if artist_id is not None:
        artist_choice = ['Albums', 'Top Songs']
        selected_artist_choice = st.sidebar.selectbox('Select artist choice', artist_choice)
                
    if selected_artist_choice is not None:
        if selected_artist_choice == 'Albums':
            artist_uri = 'spotify:artist:' + artist_id
            album_result = sp.artist_albums(artist_uri, album_type='album') 
            all_albums = album_result['items']
            col1, col2, col3 = st.columns((6,4,2))
            for album in all_albums:
                col1.write(album['name'])
                col2.write(album['release_date'])
                col3.write(album['total_tracks'])
        elif selected_artist_choice == 'Top Songs':
            artist_uri = 'spotify:artist:' + artist_id
            top_songs_result = sp.artist_top_tracks(artist_uri)
            for track in top_songs_result['tracks']:
                with st.container():
                    col1, col2, col3, col4 = st.columns((4,4,2,2))
                    col11, col12 = st.columns((10,2))
                    col21, col22 = st.columns((11,1))
                    col31, col32 = st.columns((11,1))
                    col1.write(track['id'])
                    col2.write(track['name'])
                    if track['preview_url'] is not None:
                        col11.write(track['preview_url'])  
                        with col12:   
                            st.audio(track['preview_url'], format="audio/mp3")  
                    with col3:
                        def feature_requested():
                            track_features  = sp.audio_features(track['id']) 
                            df = pd.DataFrame(track_features, index=[0])
                            df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                            with col21:
                                st.dataframe(df_features)
                            with col31:
                                polarplot.feature_plot(df_features)
                            
                        feature_button_state = st.button('Track Audio Features', key=track['id'], on_click=feature_requested)
                    with col4:
                        def similar_songs_requested():
                            token = recommendations.get_token(clientId=client_id, clientSecret=client_secret)
                            similar_songs_json = recommendations.get_track_recommendations(track['id'], token)
                            recommendation_list = similar_songs_json['tracks']
                            recommendation_list_df = pd.DataFrame(recommendation_list)
                            recommendation_df = recommendation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
                            with col21:
                                st.dataframe(recommendation_df)
                            with col31:
                                recommendations.song_recommendation_vis(recommendation_df)
                        similar_songs_state = st.button('Similar Songs',key=track['name'], on_click=similar_songs_requested)
                    st.write('----')