import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")  # Today date format : "YYYY-MM-DD"


def loadClubs():
    """open json 'clubs' file and return a list of clubs"""
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    """open json 'competitions' file and return a list of clubs"""
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def manage_over_competitions(competitions_list):
    """take a list of compétitions and return a list of competitions that are over"""
    over_competitions_list = []

    for competition in competitions_list:
        if competition["date"] < today:
            over_competitions_list.append(competition)

    return over_competitions_list


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
over_competitions = manage_over_competitions(competitions) # return a list of competitions that are over


def get_club_by_email(email):
    """take email and return a club from the list of clubs by email"""
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

    if club:  # club is found in database
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               over_competitions=over_competitions)
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
        return render_template('welcome.html',
                               club=club,
                               over_competitions=over_competitions,
                               competitions=competitions)


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

    competition_places = int(competition["numberOfPlaces"])
    club_points = int(club["points"])
    try:
        competition["numberOfPlaces"] = competition_places - places_required
        club["points"] = club_points - places_required

        manage_club_points_in_db(club)
        manage_competition_places_in_db(competition)

        flash('Great-booking complete!')
        return render_template('welcome.html',
                               club=club,
                               over_competitions=over_competitions,
                               competitions=competitions)
    except ValueError:
        # Reset competition places and club points in case of manage club or competition in db fail
        competition["numberOfPlaces"] = competition_places
        club["points"] = club_points

        flash('Sorry, there was an error with your booking. Please try again.')
        return render_template('booking.html', club=club, competition=competition)


def get_competition(form_competition_name):
    """take a competition name and return a competition from the list of competitions"""
    try:
        competition = [competition for competition in competitions if competition["name"] == form_competition_name][0]
        return competition
    except IndexError:
        return None


def get_club(form_club_name):
    """take a club name and return a club from the list of clubs"""
    try:
        club = [club for club in clubs if club["name"] == form_club_name][0]
        return club
    except IndexError:
        return None


def get_place_required(place_number):
    """take a place number and return int of places required or 0"""
    try:
        placesRequired = int(place_number)
        return placesRequired
    except ValueError:
        return int(0)


def manage_club_points_in_db(club):
    """take a club and update the club points in the database"""
    index_club = clubs.index(club)
    dict_clubs = {}

    with open('clubs.json', "w") as file_club:
        clubs[index_club]["points"] = str(club["points"])
        dict_clubs["clubs"] = clubs

        json.dump(dict_clubs, file_club, indent=4)


def manage_competition_places_in_db(competition):
    """take a competition and update the competition places in the database"""
    index_competition = competitions.index(competition)
    dict_competitions = {}

    with open('competitions.json', "w") as file_competition:
        competitions[index_competition]["numberOfPlaces"] = str(competition["numberOfPlaces"])
        dict_competitions["competitions"] = competitions

        json.dump(dict_competitions, file_competition, indent=4)


@app.route('/displayClubsList', methods=['GET'])
def displayClubsList():
    if clubs:
        return render_template('display_clubs.html', clubs=clubs)
    else:
        flash("Sorry, there is no club in data base")
        return redirect(url_for("index"))


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
