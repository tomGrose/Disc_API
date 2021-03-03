from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Disc, Company
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///discs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "turtlezrock"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/api/discs")
def get_discs():
    """ Return all the discs in the directory"""

    discs = Disc.query.all()
    ser_discs = []
    for disc in discs:
        s_disc = disc.serialize()
        ser_discs.append(s_disc)
    data = {"discs": ser_discs}
    return (jsonify(data), 200)

@app.route("/api/discs/<disc_name>")
def search_discs(disc_name):
    """ Return all discs that match the name. Many discs have the same name but a different plastic """

    discs = Disc.query.filter(Disc.name.ilike(f"{disc_name.lower()}%")).all()
    if len(discs) == 0:
        data = {"Error": "Sorry but no discs similiar to this spelling were found. Please check your spelling and try again"}
        return (jsonify(data), 404)
    ser_discs = []
    for disc in discs:
        s_disc = disc.serialize()
        ser_discs.append(s_disc)
    data = {"discs": ser_discs}
    return (jsonify(data), 200)


@app.route("/api/companies")
def get_companies():
    """ Return all the companies in the directory """

    companies = Company.query.all()
    ser_companies = []
    for c in companies:
        s_company = c.serialize()
        ser_companies.append(s_company)
    data = {"Companies": ser_companies}
    return (jsonify(data), 200)


@app.route("/api/companies/<company_name>")
def get_disc(company_name):
    """Return all the discs from a company"""

    discs = Disc.query.filter(Disc.company_name.ilike(company_name.lower())).all()
    ser_discs = []
    if len(discs) == 0:
        data = {"Error": "Sorry but this company was not found. Check your spelling and try again"}
        return (jsonify(data), 404)
    for disc in discs:
        s_disc = disc.serialize()
        ser_discs.append(s_disc)
    data = {"Company": company_name, "Discs": ser_discs}
    return (jsonify(data), 200)
