import requests
from bs4 import BeautifulSoup
from exceptions import BroadQueryError, QueryError

def get_athlete_pb(athlete_id):
    '''
    Returns a list of personal bests for the specified athlete id.

            Parameters:
                    - 'athlete_id' (int): reference id of athlete (used by PowerOf10)

            Returns:
                    - 'pb' (list): List of personal bests
                        - 'event' (str): Event name
                        - 'value' (float): Personal best in given event
    '''
    if athlete_id is None:
        raise ValueError('Please input a valid athlete id.')

    url = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid={athlete_id}'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    
    if soup.find('div', {'id': 'pnlMainGeneral'}).text.replace('\n', '') == 'Profile not found':
        raise ValueError('Profile not found. Please input a valid athlete id')

    try:
        athlete_pb = soup.find('div', {'id': 'cphBody_divBestPerformances'}).find_all('tr')
        pb = []
        for i in athlete_pb:
            if i.find('b').text != 'Event':
                pb.append({
                    'event': i.find('b').text,
                    'value': i.find_all('td')[1].text
                })
    except Exception as e:
        pb = []

    return pb