import requests
from datetime import datetime
import PySimpleGUI as sg
import sys

#THX to UMAN231 for the help getting this done.

#settings
unit = 1 #1=metric, 0=imperial
v = 'v0.2'
sg.ChangeLookAndFeel('SystemDefault')
timeout = 1800*1000
sokText = 'Sök'
apiKey = '9bf26205db1db79d1aa8083ad6c981ba'
#end settings

if unit == 0:
    units = 'imperial'
    grader = '°F'
else:
    units = 'metric'
    grader = '°C'




layout = [[sg.Text("City")],
          [sg.Input(key='-INPUT-0')],
          [sg.Multiline(size=(45,9), key='-OUTPUT-0')],
          [sg.Button('Search', key='update', bind_return_key=True), sg.Button('Close')]]

window = sg.Window(f'Weather on location {v}', layout, resizable=True, alpha_channel=1, grab_anywhere=False)

while True:
    event, values = window.read(timeout=timeout)
    if event == sg.WINDOW_CLOSED or event == 'Close':
        break
    stadIn = values['-INPUT-0']
    urlStad = f'https://api.openweathermap.org/geo/1.0/direct?q={stadIn}&limit=1&appid={apiKey}'
    respStad = requests.get(url=urlStad)
    dataStad = respStad.json()
    try:
        stad = dataStad[0]['local_names']['feature_name']
        lat = dataStad[0]['lat']
        lon = dataStad[0]['lon']
    except:
        window['-OUTPUT-0'].update('Could not get the weather for the city provided!')
        continue
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&lang=en&exclude=minutely,hourly,daily,alerts&units={units}&appid={apiKey}'
    resp = requests.get(url=url)
    data = resp.json()
    try:
        solupp = datetime.fromtimestamp(data['current']['sunrise']).strftime('%H:%M')
        solner = datetime.fromtimestamp(data['current']['sunset']).strftime('%H:%M')
        vaderNu = data['current']['weather'][0]['description']
        temp = round(data['current']['temp'],1)
        typtemp = round(data['current']['feels_like'],1)
        uvindex = data['current']['uvi']
        vindstyrka = round(data['current']['wind_speed'], 1)
        funktighet = data['current']['humidity']
        hpa = data['current']['pressure']
        sokText = 'Uppdatera'
    except:
        window['-OUTPUT-0'].update('Could not get the weather for the city provided!')
        continue
        
    textUt = f'''{stad}\nSun rises at {solupp}\nSun sets at {solner}\nWeather now is {vaderNu} and windspeed is {vindstyrka}m/s\nIt's {temp}{grader} with RealFeel as {typtemp}{grader}\nUV-Index: {uvindex}\nHumidity: {funktighet}%\nPreasure: {hpa}hPa'''

    window['-OUTPUT-0'].update(textUt)
    
window.close()
