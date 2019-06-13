import requests
from bs4 import BeautifulSoup
from operator import itemgetter

PYLATAM_URL = 'https://vote.pylatam.org/votes/'
SESSION_ID = ''

def convert_to_float(percentage):
    return float(format(percentage.replace('%', ''))[:3])

def get_talks(talks=[]):
    re = requests.get(PYLATAM_URL, cookies={
        'sessionid': SESSION_ID
    })

    if re.status_code == 200:
        soup = BeautifulSoup(re.text, 'html.parser')

        if soup:
            tbody = soup.find('tbody')

            for tr in tbody.find_all('tr'):
                talk = dict()
                title = tr.find('td').find('a')

                if title:
                    talk['title'] = title.text

                    for tr2 in tr.find_all('tr'):
                        deny = tr2.find('td', {'class': 'percentage-bar__deny'})['width']
                        maybe = tr2.find('td', {'class': 'percentage-bar__maybe'})['width']
                        approve = tr2.find('td', {'class': 'percentage-bar__approve'})['width']

                        talk['deny'] = convert_to_float(deny)
                        talk['maybe'] = convert_to_float(maybe)
                        talk['approve'] = convert_to_float(approve)

                    talks.append(talk)

        return talks

if __name__ == '__main__':
    talks = get_talks()
    talks.sort(key=itemgetter('approve'), reverse=True)

    for index, talk in  enumerate(talks, 1):
        message = f"{index}.- {talk['title']} {talk['approve']}"
        print(message)
