import requests
from bs4 import BeautifulSoup
from exceptions import BroadQueryError, QueryError

def get_ids(firstname=None, surname=None, club=None):
    '''
    Returns a list of athlete IDs with the inputted firstname, surname or club.

            Parameters:
                    - 'firstname' (str): Optional first name argument
                    - 'surname' (str): Optional surname argument
                    - 'club' (str): Optional club argument

            Returns:
                    - 'athlete_ids' (list): List of athlete IDs (int)
    '''
    url = f'https://www.thepowerof10.info/athletes/athleteslookup.aspx?'
    if surname is not None:
        url += f'surname={surname.replace(" ","+")}&'
    if firstname is not None:
        url += f'firstname={firstname.replace(" ","+")}&'
    if club is not None:
        url += f'club={club.replace(" ","+")}'

    if firstname is None and surname is None and club is None:
        raise QueryError('Please input a firstname, surname or club')
    
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    results = soup.find('div', {'id': 'cphBody_pnlResults'}).find_all('tr')
    
    if 'cphBody_lblResultsErrorMessage' in str(results[0]):
        raise BroadQueryError(results[0].text)

    athlete_ids = []
    for r in results[1:-1]:
        row = BeautifulSoup(str(r), 'html.parser').find_all('td')
        athlete_id = str(row[7]).split('"')[3].split('=')[1]
        athlete_ids.append(athlete_id)

    if not athlete_ids:
        raise QueryError('No athletes found. Use broader search terms or amend your queries.')

    return athlete_ids


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