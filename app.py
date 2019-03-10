# import dependices 
from flask import Flask, jsonify
import numpy as np
from sqlalchemy import create_engine
# from sqlalchemy.ext.delarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd

#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# create an app
app = Flask(__name__)

# home page
@app.route("/")
def home():
    print()
    return(
        f"Surfs up dude! Use this API to see which days are best to catch those epic waves!<br>"
        f"Available routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/ + start date<br>"
        f"/api/v1.0/ + start date/ + end date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    DateandPrcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > "2016-08-31").\
    order_by(Measurement.date.desc()).all()
    dataDict = {date: prcp for date, prcp in DateandPrcp}
    return jsonify(dataDict)



@app.route("/api/v1.0/stations")
def stations():
    result = session.query(Station.station).all()
    station = list(np.ravel(result))
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    maxDate = session.query(func.max(Measurement.date)).all()
    mDate = maxDate[0][0]
    d = dt.datetime.strptime(mDate, '%Y-%m-%d').date()
    yearAgo = ((d - relativedelta(years=1)).strftime('%Y-%m-%d'))

    tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >= yearAgo).\
    filter(Measurement.date <= mDate).all()    
    tobsData = list(np.ravel(tobs))
    return jsonify(tobsData)

@app.route("/api/v1.0/<start>")
def startDate(start):
    tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >= start).all()

    startData_df = pd.DataFrame(tobs)
    
    tmin = startData_df.min()
    tavg = startData_df.mean()
    tmax = startData_df.max()
    all = [tmin, tavg, tmax]
    all2 = list(np.ravel(all))

    return jsonify(all2)


@app.route("/api/v1.0/<start>/<end>")
def startANDendDate(start, end):
    tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    startendData_df = pd.DataFrame(tobs)
    
    tmin = startendData_df.min()
    tavg = startendData_df.mean()
    tmax = startendData_df.max()
    all = [tmin, tavg, tmax]
    all2 = list(np.ravel(all))

    return jsonify(all2)


if __name__ == "__main__":
    app.run(debug=True)