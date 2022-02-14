from flask import Flask
import datetime
import pytz
app = Flask(__name__)

# root route. Displays a short description of the app and the /time route.
@app.route('/')
def index():
    return '''<h1>Welcome to the Time App!</h1>
    <p>This is a simple app that returns the current time.</p>
    <p>Please go to <a href="/time">/time</a> to see the time.</p>'''
    
# /time route. Returns the current time in various timezones.
@app.route('/time')
def time():
    # display the current time in Eastern, Central, and Pacific timezones.
            return '''<h4>The current time in Eastern, Central, and Pacific timezones:</h4>
    <p>Eastern: {}</p>
    <p>Central: {}</p>
    <p>Pacific: {}</p>'''.format(
        # get the current time in Eastern, Central, and Pacific timezones.
        get_time('America/New_York'),
        get_time('America/Chicago'),
        get_time('America/Los_Angeles')
    )
    
# get_time function. Returns the current time in a given timezone.
def get_time(timezone):
    # get the current time in the given timezone.
    utc_dt = datetime.datetime.now(tz=pytz.utc)
    # get the current time in the given timezone.
    local_dt = utc_dt.astimezone(pytz.timezone(timezone))
    # return the current time in the given timezone.
    return local_dt.strftime('%H:%M:%S')



app.run(host='0.0.0.0',
        port=8080,
        debug=True)
