import random
import re
import sys
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time
from datetime import datetime, date
from dateutil.rrule import *

def update_countdown():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('index.html'), 'countdown'))

# initialize flask
app = Flask(__name__)
turbo = Turbo(app)

# Fecha objetivo
end_date = datetime(2022,8,1)
myset = rruleset()


#Feriados
myset.exdate(datetime(2022,2,28))
myset.exdate(datetime(2022,3,1))
myset.exdate(datetime(2022,4,14))
myset.exdate(datetime(2022,4,15))
myset.exdate(datetime(2022,4,18))
myset.exdate(datetime(2022,5,1))
myset.exdate(datetime(2022,5,16))
myset.exdate(datetime(2022,6,19))
myset.exdate(datetime(2022,7,18))


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_countdown).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.context_processor
def inject_countdown():

    myrule=rrule(freq=DAILY, until=end_date, byweekday=[MO,TU,WE,TH,FR], byhour=0, byminute=0, bysecond=0, cache=True)
    myset.rrule(myrule)

    tnow = datetime.now()

    w_days = myset.count()
    w_hours = w_days * 8
    sod=rrule(freq=DAILY, count=1, byhour=10, byminute=0, bysecond=0, cache=True)
    eod=rrule(freq=DAILY, count=1, byhour=18, byminute=0, bysecond=0, cache=True)
    w_hours = w_minutes = w_seconds = 0

    if (eod[0] > tnow and eod[0] < sod[0]):
        today_left = eod[0] - tnow
        w_hours, remainder = divmod(today_left.seconds+1, 3600)
        w_minutes, w_seconds = divmod(remainder, 60)

    w_hours = w_days * 8 + w_hours

    tdif = end_date - tnow
    hours, remainder = divmod(tdif.seconds+1, 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "days":tdif.days,
        "hours": tdif.days*24 + hours,
        "minutes":'%02d' % minutes,
        "seconds":'%02d' % seconds,
        "w_days":w_days,
        "w_hours":w_hours,
        "w_minutes":'%02d' % w_minutes,
        "w_seconds":'%02d' % w_seconds,
        "now": tnow.strftime("%d/%m/%Y %H:%M:%S")
    }