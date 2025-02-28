import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


def get_club_by_email(email):
    try:
        club = [club for club in clubs if club['email'] == email][0]
        return club
    except IndexError:
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = get_club_by_email(request.form['email'])
    if club:    # club is found in database
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Sorry, we couldn't find that email.")
        return redirect(url_for("index"))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():

    competition = get_competition(request.form["competition"])
    club = get_club(request.form["club"])
    places_required = get_place_required(request.form["places"])

    if places_required < 1:
        flash('Sorry, select a number of places greater than 0.')
        return redirect(url_for("book", competition=competition["name"], club=club["name"]))
    elif int(places_required) > int(club["points"]):
        flash("Sorry, your club doesn't have enough points.")
        return redirect(url_for("book", competition=competition["name"], club=club["name"]))
    elif int(places_required) > int(competition["numberOfPlaces"]):
        flash("Sorry, you cannot reserve more places than are available.")
        return redirect(url_for("book", competition=competition["name"], club=club["name"]))
    elif int(places_required) > int(12):
        flash("Sorry, the maximum number of places per club per competition is : 12.")
        return redirect(url_for("book", competition=competition["name"], club=club["name"]))

    try:
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
        club["points"] = int(club["points"]) - places_required

        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    except ValueError:
        flash('Sorry, there was an error with your booking. Please try again.')
        return render_template('booking.html', club=club, competition=competition)


def get_competition(form_competition_name):
    try:
        competition = [competition for competition in competitions if competition["name"] == form_competition_name][0]
        return competition
    except IndexError:
        return None


def get_club(form_club_name):
    try:
        club = [club for club in clubs if club["name"] == form_club_name][0]
        return club
    except IndexError:
        return None


def get_place_required(place_number):
    try:
        placesRequired = int(place_number)
        return placesRequired
    except ValueError:
        return int(0)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
