from flask import Flask, session, url_for, flash, redirect, request, render_template

from . import app
from . import models
from . import profiles
from . import forms
from . import recurse
from . import events

from .oauth import auth, get_login, login_required


def session_init(resp, next_url):
    session['oauth_token'] = (resp['access_token'], resp['refresh_token'])

    me = auth.get('people/me')
    if me.status is not 200:
        flash('Could not get the user info!')
        print('Unexpected status of oauth request: ' + str(me.status))
        return redirect(next_url)

    session["login"] = {}
    session["login"]["id"] = me.data["id"]
    session["login"]["name"] = me.data["first_name"] + " " + me.data["last_name"]
    session["login"]["avatar"] = me.data["image"]

    profiles.get_login_profile(me)


@app.route('/oauth_authorized')
def oauth_authorized():
    next_url = request.args.get('return_url') or url_for('profile')

    resp = auth.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
        return redirect(next_url)

    session_init(resp, next_url)

    return redirect(next_url)


@app.route('/login')
def login():
    if get_login():
        flash('You are already logged in.')
        return redirect(request.referrer or url_for('profile'))
    else:
        afterward = request.args.get('return_url') or request.referrer or None
        landing = url_for('oauth_authorized', return_url=afterward, _external=True)
        return auth.authorize(callback=landing)


@app.route('/logout')
def logout():
    session.pop('login', None)

    return redirect(url_for('index'))


@app.route("/")
def index():
    login = get_login()

    if login is not None:
        client = app.test_client()
        return client.get('/profile/', headers=list(request.headers))
    else:
        return render_template('index.html', profile=None)


@app.route('/profile/<int:uid>/')
@app.route('/profile/')
@login_required
def profile(uid=None, login=None):
    recurse.fetch_batches_if_outdated()

    if uid is None:
        uid=login["id"]

    profile = profiles.get_profile_by_uid(uid)
    if profile is None:
        return '<h1>Profile with id: %d has not been created!</h1>' % uid

    scores = profiles.get_scores()
    profile["score"] = profiles.get_scores(uid)[0]["score"]
    profile["position"] = [i for i, j in enumerate(scores) if j["_id"] == uid][0] + 1
    profile["level"] = models.get_level_by_score(profile["score"])

    event_list = events.get_events(uid)
    for event in event_list:
        event["goals_list"] = ["%s" % models.goals[int(id)] for id in event["goals_list"]]
        event["target_profile"] = profiles.get_profile_by_name(event["target_name"])

    return render_template('profile.html', login=login,
                                           profile=profile,
                                           goals=models.goals,
                                           events=event_list)


@app.route('/submit', methods=["GET", "POST"])
@login_required
def submit(login=None):
    recurse.fetch_batches_if_outdated()
    recursers = recurse.get()

    profile = profiles.get_profile_by_uid(login["id"])
    profile["recursers_number"] = len(recursers)
    profile["recursers"] = recursers

    form = forms.GoalForm()

    persons = [x["first_name"] + " " + x["last_name"] for x in recursers]
    persons.sort()

    if request.method == 'POST' and form.validate():
        chosen_goals = form.goals_mcheckbox.data
        chosen_person = form.person_text.data

        target_profile = profiles.get_profile_by_name(chosen_person)

        if chosen_person not in persons:
            flash("Sorry but the person you selected does not exist!")
            return redirect(url_for('profile', uid=login["id"]))

        buddies = events.get_buddies_by_uid(login["id"])
        if chosen_person in buddies:
            flash("You cannot submit the same person more than once!")
            return redirect(url_for('profile', uid=login["id"]))

        if target_profile is None:
            target_profile_id = None
        else:
            target_profile_id = target_profile["_id"]

        event = events.init_event(events.pair,
                                  login["id"],
                                  target_profile_id,
                                  chosen_person,
                                  chosen_goals)
        events.create(event)

        profiles.set_goals(login["id"], chosen_goals, 1)

        flash("Your request was processed!")
        return redirect(url_for('profile', uid=login["id"]))


    return render_template('submit.html', login=login,
                                          profile=profile,
                                          goals=models.goals,
                                          form=form,
                                          persons=persons)


@app.route('/scoreboard')
@login_required
def scoreboard(login=None):
    recurse.fetch_batches_if_outdated()

    profile = profiles.get_profile_by_uid(login["id"])

    score_data = profiles.get_scores()
    for user in score_data:
        user["profile"] = profiles.get_profile_by_uid(user["_id"])
        user["level"] = models.get_level_by_score(user["score"])

    return render_template('scoreboard.html', login=login,
                                              profile=profile,
                                              scoreboard=score_data)


@app.route('/feed')
@login_required
def feed(login=None):
    recurse.fetch_batches_if_outdated()

    profile = profiles.get_profile_by_uid(login["id"])

    event_list = events.get_events()
    for event in event_list:
        event["goals_list"] = ["%s" % models.goals[int(id)] for id in event["goals_list"]]
        event["target_profile"] = profiles.get_profile_by_name(event["target_name"])

    return render_template('feed.html', login=login,
                                        goals=models.goals,
                                        profile=profile,
                                        events=event_list)


@app.route('/invite/<string:name>/')
@login_required
def invite(name=None, login=None):
    recurse.fetch_batches_if_outdated()

    profile = recurse.get_by_name(name)

    return '<h1>This module is in development phase</h1>' \
           '<h3>Recognize him? This user has not registered yet.</h3>' \
           '<img src="{}">' \
           '<h3>Tell him to join in! <a href="mailto:{}">{}</a></h3>'.format(profile["image"], profile["email"], profile["email"])


@app.route('/unsubmit/<string:eid>/')
@login_required
def unsubmit(eid=None, login=None):
    recurse.fetch_batches_if_outdated()

    profile = profiles.get_profile_by_uid(login["id"])

    # TODO: Check submitter ID

    goals = events.get_goals_by_eid(eid)
    profiles.set_goals(login["id"], goals, 0)
    events.remove_by_eid(eid)

    flash("Record was unsubmitted!")
    return redirect(url_for('profile', uid=login["id"]))


@app.route('/update_batches')
@login_required
def update_batches(login=None):
    recurse.fetch_batches_if_outdated()

    recursers = recurse.get()

    flash("Batch info was updated! Persons fetched: {}".format(len(recursers)))
    return redirect(url_for('profile', uid=login["id"]))


@app.before_request
def before_request():
    if request.url.startswith('https://'):
        url = request.url.replace('https://', 'http://', 1)
        code = 301
        return redirect(url, code=code)
