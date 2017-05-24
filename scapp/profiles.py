from flask import json, session
from . import mongo
from . import models

def init_from_me(d):
    profile = {}

    # default fields
    profile["name"] = '{first_name} {last_name}'.format(**d)
    profile["image"] = d["image"]
    profile["interests"] = d["interests"]
    profile["batch_id"] = d["batch_id"]
    profile["_id"] = d["id"]

    profile["location"] = d["current_location"]["ascii_name"]
    profile["email"] = d["email"]
    profile["job"] = d["job"]
    profile["github"] = d["github"]
    profile["twitter"] = d["twitter"]
    profile["interests"] = d["interests"]

    profile["goals"] = [0 for x in range(len(models.goals))]
    profile["history"] = []

    return profile


def get_login_profile(me):
    # TODO: This is not atomic
    profile = get_profile_by_uid(me.data["id"])
    if profile is None:
        profile = init_from_me(me.data)
        create(profile)

    return profile


def create(profile):
    return mongo.db.profiles.insert_one(profile)


def get_profile_by_uid(uid):
    return mongo.db.profiles.find_one({"_id": uid})


def get_profile_by_name(name):
    return mongo.db.profiles.find_one({"name": name})


def set_goals(uid, goals, bit):
    query = {"_id": uid}

    updates = {}
    updates["$set"] = {"goals.%s" % goal: bit for goal in goals}

    mongo.db.profiles.find_one_and_update(query, updates)


def get_scores(uid=None, batch_ids=None):

    filter = {}
    if batch_ids is not None:
        filter = { "$or": [ {"batch_id": uid } for uid in batch_ids ]}

    if uid is not None:
        filter = { "_id": uid }

    cursor = mongo.db.profiles.aggregate([
        { "$match": filter },
        { "$project": {
            "name": "$name",
            "score": { "$sum": "$goals" } } },
        { "$sort": { "score": -1 } },
        { "$out": "scoreboard" }
    ])

    scores = mongo.db.scoreboard.find()
    scores = list(scores)

    return scores
