# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import os
import re
import requests

APPID = os.getenv("WEATHER_KEY")
debug = True


def make_request(request, location, unit):
    r = requests.get("http://api.openweathermap.org/data/2.5/{0}?".format(request), {"zip": "{0},us".format(location),"units": unit, "APPID": APPID})
    json_data = r.json()
    return json_data


def current_conditions(zip, units='metric'):
    """Gets current conditions of the zip provided."""
    zip = zip.strip()
    if len(zip) != 5:
        raise ValueError('Invalid zip.')
    else:
        weather_data = make_request('weather', zip, units)

    if weather_data['cod'] == 200:
        descriptions = weather_data['weather'][0]
        measurements = weather_data['main']
        winds = weather_data['wind']
        results = {'descriptions': {
            'brief': descriptions['main'], 'long': descriptions['description']}}
        return results
    else:
        return {'status': weather_data['cod'], "message": weather_data['message']}


def wind_direction(deg):
    if deg == 0:
        return 'n' 
    elif deg > 0 and deg < 90:
        return 'ne'
    elif deg == 90:
        return 'e'
    elif deg > 90 and deg < 180:
        return 'se'
    elif deg == 180:
        return 's'
    elif deg > 180 and deg < 270:
        return 'sw'
    elif deg == 270:
        return 'w'
    elif deg > 270 and deg < 359:
        return 'nw'
    else:
        return 'unavailable' 


def five_day(zip, units="metric"):
    """Retreives five day weather forecast"""
    day_of_week = datetime.date.today().weekday()
    weather_data = make_request('forecast/daily', zip, units)
    names = ('Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday')
    result = {}
        if weather_data['cod'] == '200':
        result['city'] = weather_data['city']['name']
        for i in range(1, 6):
            day = weather_data['list'][i]
            result[names[day_of_week]] = {'high': day['temp']['max'],\
            'low': day['temp']['min'],\
            'humidity': day['humidity'] ,\
            'descriptions': {'brief': day['weather'][0]['main'], 'details': day['weather'][0]['description']},\
            'icons': day['weather'][0]['icon'],\
            'winds': {'speed': day['speed'], 'direction': wind_direction(day['deg'])}
            }
            day_of_week += 1
        return result
    else:
        return {'status': weather_data['cod'], 'message': weather_data['message']}