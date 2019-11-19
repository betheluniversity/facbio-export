import requests
import dataset
import xml.etree.ElementTree as ET

from config import config

banner_db = dataset.connect(config['BANNER_CONSTR'], reflect_metadata=False)
table = banner_db[config['TABLE_NAME']]

xml_data = requests.get(config['BIO_URL'])
root = ET.fromstring(xml_data.content)

for page in root.findall('system-page'):
    try:
        username = page.find('author').text
        # some authors had a value like 'abc12345@bethel.edu'
        if '@bethel.edu' in username:
            username = username.strip('@bethel.edu')
        path = page.find('path').text
        url = 'https://www.bethel.edu{}'.format(path)
        data = {
            'username': username,
            'url': url
        }
        try:
            table.upsert(data, ['username'], ensure=False)
        except:
            print('Skipping user: {}').format(username)

    # deactivated bio's dont' have an author, so '.text' will throw AttributeError.
    # I determined with Lisa to skip these ones -- ej
    except AttributeError:
        continue
