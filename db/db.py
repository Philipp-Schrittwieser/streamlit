import streamlit as st
import pymongo
import uuid

db_conn_string = st.secrets.DB_CONNECTION_STRING


def connect_db():
    client = pymongo.MongoClient(db_conn_string)
    db = client.get_database("school")
    return db

def new_kahoot(id, current_page, topic, user_text, user_youtube_link, csv):
    st.session_state.db.kahoots.insert_one({
        "_id": id,
        "current_page": current_page,
        "topic": topic,
        "user_text": user_text,
        "user_youtube_link": user_youtube_link,
        "csv": csv
})

def return_kahoot(id):
    return st.session_state.db.kahoots.find_one({"_id": id})