import bs4
import requests

def get_info(id):
    url = f'https://apkpure.net/null/{id}/versions'
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    title = soup.find('div', class_='app-name').find('h1').text
    type = soup.find('div', class_='app-name').find('span').text.lower()
    developer = soup.find('a', class_='developer').text
    date = soup.find('div', class_='date').text.lower()
    versions = []
    for i in soup.find_all('li', class_='version'):
        url = 'https://apkpure.net/' + i.find('a', class_='download-btn')['href']
        version = i.find('div', class_='code-info').find('span', class_='name').text.lower()
        version_code = i.find('div', class_='code-info').find('span', class_='code').text.lower().replace('(', '').replace(')', '')
        type = i.find('div', class_='code-info').find('span', class_='tag').text.lower()
        t = i.find('div', class_='additional-info').find_all('span')
        date = None
        size = None
        android_version = None
        if len(t) >= 1:
            date = t[0].text.lower()
        if len(t) >= 2:
            size = t[1].text.lower()
        if len(t) >= 3:
            android_version = t[2].text.lower()
        versions.append({
            'url': url,
            'version': version,
            'version_code': version_code,
            'type': type,
            'date': date,
            'size': size,
            'android_version': android_version
        })
    return {
        'versions': versions,
        'title': title,
        'type': type,
        'developer': developer,
        'date': date
    }

def download(url, path_or_file_like):
    file = None
    if isinstance(path_or_file_like, str):
        file = open(path_or_file_like, 'wb')
    else:
        file = path_or_file_like
    r = requests.get(url)
    soop = bs4.BeautifulSoup(r.text, 'html.parser')
    download_url = soop.find('a', class_='download-start-btn')['href']
    r = requests.get(download_url)
    file.write(r.content)
    file.close()