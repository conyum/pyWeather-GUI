import requests
import PySimpleGUI as sg
import sys
import os
from datetime import datetime
from json import (load as jsonload, dump as jsondump)
from os import path
from sys import platform

#THX to UMAN231 for the help getting this done.

#settings
v = 'v0.3'
sg.ChangeLookAndFeel('SystemDefault')
timeout = 1800*1000
sokText = 'Sök'
apiKey = '9bf26205db1db79d1aa8083ad6c981ba'
cel = '°C'
far = '°F'
sN = os.path.basename(__file__)
if platform == "linux" or platform == "linux2":
    devNull = "/dev/null"
elif platform == "darwin":
    devNull = "/dev/null"
elif platform == "win32":
    devNull = "NUL"

SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'city': 'new york', 'unitf': True, 'unitm': False, 'apikey' : apiKey}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'city': '-INPUT-0', 'unitf': '-UNITF-', 'unitm': '-UNITM-', 'apikey' : '-APIKEY-'}

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'\n\ni found No settings file... \nI will create one for you\n\n\n', keep_on_top=True, background_color='white', text_color='black')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


def save_settings(settings_file, settings, values):
    if values:
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')
    
def create_settings_window(settings):

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  [sg.Text('Settings', font='Any 15')],
                [TextLabel("City"), sg.Input(key='-INPUT-0')],
                [TextLabel('Unit'),sg.Radio(f'{cel}', "R1", key="-UNITM-"), sg.Radio(f'{far}', "R1", key="-UNITF-")],
                [TextLabel('API-key'),sg.Input(key='-APIKEY-')],
                [sg.Button('Save & exit'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)

    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating the program from settings. Key = {key}')

    return window

def create_main_window(settings):
    layout = [[sg.Multiline('Please use the update button to initiate the program', size=(45,9), key='-OUTPUT-0')],
              [sg.Button('Update', key='update', bind_return_key=True), sg.Button('Exit'), sg.Button('Change Settings')]]
    return sg.Window(f'Weather in city {v}', layout, resizable=True, alpha_channel=1, grab_anywhere=False)

def main():
    window, settings = None, load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    while True:
        if window is None:
            window = create_main_window(settings)
        
        event, values = window.read(timeout=timeout)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Change Settings':
            event, values = create_settings_window(settings).read(close=True)
            if event == 'Save & exit':
                window.close()
                save_settings(SETTINGS_FILE, settings, values)
                os.system(f"python {sN} > {devNull} 2>&1")
                break
            
        if settings['unitf'] == True:
            units = 'imperial'
            grader = far
        if settings['unitm'] == True:
            units = 'metric'
            grader = cel
        
        stadIn = settings['city']
        stringKey = settings['apikey']
        urlStad = f'https://api.openweathermap.org/geo/1.0/direct?q={stadIn}&limit=1&appid={stringKey}'
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
            sokText = 'Update'
        except:
            window['-OUTPUT-0'].update('Could not get the weather for the city provided!')
            continue
        
        textUt = f'''{stad}\nSun rises at {solupp}\nSun sets at {solner}\nWeather now is {vaderNu} and windspeed is {vindstyrka}m/s\nIt's {temp}{grader} with RealFeel as {typtemp}{grader}\nUV-Index: {uvindex}\nHumidity: {funktighet}%\nPreasure: {hpa}hPa'''
        
        
        window['-OUTPUT-0'].update(textUt)
    
    window.close()
main()
