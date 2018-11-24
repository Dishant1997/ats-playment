from pymongo import MongoClient
import json
import logging
from bson.objectid import ObjectId
from settings import global_data
from datetime import datetime
import requests

client = MongoClient('localhost', 27017)
db = MongoClient('mongodb://apply:abcd1234@ds043487.mlab.com:43487/heroku_vg2c9pkg')


"""
db.apply.submissions

{
    _id: ...,
    username: String,
    creation_date: Date(),
    submission_date: Date();
    submitted: Boolean,
    state: int # 0 = nothing submitted, 1 = email, name, web, projects submitted; 2 = video 1 submitted; 3 = video 2 submitted = final state,
    email: String,
    name: String,
    comment: String,
    
    web: String,
    location: String,
    projects: String,
    
    video1_token: String, # ziggeo token
    video2_token: String, # ziggeo token
    
    ratings: Object # Associative array mapping twitter handle of admin to rating
    tags: Array
}

"""


    
