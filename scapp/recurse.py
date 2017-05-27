"""
Scheduler job sets recursers data dirty each monday
It gets refreshed at next authorization based on a 'dirty' flag
Flask debug mode arranges two job instead of one and that is expected
"""

from apscheduler.schedulers.background import BackgroundScheduler
from .oauth import auth
from . import mongo

up_to_date = False

def set_dirty():
    global up_to_date

    print("Hey!")
    up_to_date = False

sched = BackgroundScheduler()
sched.add_job(set_dirty, 'cron', day_of_week='mon')
sched.start()


def fetch_batches_if_outdated():
    global up_to_date

    if up_to_date is False:
        fetch_batches()
        up_to_date = True
        print("Batches were updated!")


def fetch_batches():
    """
    !!! This function REQUIRES valid oauth token !!!
    Fill out recursers_data with up-to-date values
    """
    global recursers

    batches = auth.get('batches')
    if batches.status is not 200:
        print('Unexpected status of oauth request: ' + str(batches.status))
        return
    current_batch_id = batches.data[0]["id"]

    recursers = []
    for batch_id in range(0, current_batch_id + 1):
        recursers1 = auth.get('batches/' + str(batch_id) + '/people')
        if recursers1.status is 200:
            recursers.extend(recursers1.data)

    create(recursers)


def create(recursers):
    mongo.db.recursers.drop()
    return mongo.db.recursers.insert(recursers)


def get():
    recursers = mongo.db.recursers.find( { } )
    recursers = list(recursers)

    return recursers

def get_by_name(name):
    first_name, last_name = name.split(' ', 1)

    recurser = mongo.db.recursers.find_one( {
        "$and": [ { "first_name": first_name },
                  { "last_name": last_name } ]
    } )

    return recurser
