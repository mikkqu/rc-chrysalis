from . import mongo
from . import profiles
from bson.objectid import ObjectId

pair = 1
meet = 2
invite = 3
join = 4
levelup = 5
score = 6


def init_event(event_type, source_id=None, target_id=None, submit_date=None,
               target_name=None, goals_list=None, work_type=None, details=None):
    event = {
        "event_type": event_type,
        "date": submit_date,
        "source_profile": profiles.get_profile_by_uid(source_id),
        "target_profile": profiles.get_profile_by_uid(target_id),
        "target_name": target_name,
        "work_type": work_type,
        "details": details
    }

    if goals_list is not None:
        event["goals_list"] = goals_list

    return event


def create(event):
    return mongo.db.events.insert_one(event)


def get_events(uid=None):
    query = {}

    if uid is not None:
        query = {
            "$or": [
                {"source_profile._id": uid},
                {"target_profile._id": uid}
            ]
        }

    entries = mongo.db.events.find(query)
    entries = list(entries)

    return entries


def get_buddies_by_uid(uid):
    entries = mongo.db.events.find( {"source_profile._id": uid } )
    entries = list(entries)

    buddies = [x["target_name"] for x in entries]

    return buddies


def get_goals_by_eid(eid):
    entry = mongo.db.events.find_one( {"_id": ObjectId(eid) } )
    print(eid)

    return entry["goals_list"]


def remove_by_eid(eid):
    return mongo.db.events.delete_one( {"_id": ObjectId(eid)} )