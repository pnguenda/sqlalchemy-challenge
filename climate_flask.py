from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# setting up our database 
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables  
Base.prepare(engine, reflect=True)

# Save references to each table
# Measurement classes
ME = Base.classes.measurement
# Station classes
ST = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# flask set up
app = Flask(__name__)

# Flask routes
# Listing all available api routes
@app.route("/")
def welcome():
    return (
        f"Availabile Routes: <br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs <br>"
    )

# Design a query to retrieve the last 12 months of precipitation data and plot the results

@app.route("/api/v1.0/precipitation")
def precipitation():
    #querying the percipitation
    last_12_months = session.query(ME.date).order_by(ME.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_scores = session.query(ME.date, ME.prcp).\
    filter(ME.date >= year_ago, ME.prcp !=None).\
    order_by(ME.date).all()
    
    return jsonify(dict(prcp_scores))
    

@app.route("/api/v1.0/stations")
def stations():
    session.query(ME.station).distinct().count()
    active_stat = session.query(ME.station,func.count(ME.station)).\
                               group_by(ME.station).\
                               order_by(func.count(ME.station).desc()).all()
    return jsonify(dict(active_stat))
    
    
@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    yearly_temp = session.query(ME.tobs).\
      filter(ME.date >= year_ago, ME.station == 'USC00519281').\
      order_by(ME.tobs).all()
    
 #returnig the list in a jsonified formart

    temp_list = list(np.ravel(yearly_temp))
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)