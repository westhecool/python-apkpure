import bs4
import requests
import os

def get_info(id):
    url = f'https://apkpure.net/null/{id}/versions'
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    title = None
    type = None
    if soup.find('div', class_='app-name'):
        title = soup.find('div', class_='app-name').find('h1').text.strip()
        type = soup.find('div', class_='app-name').find('span').text.strip().lower()
    elif soup.find('a', class_='ver_title'):
        title = soup.find('a', class_='ver_title').text.strip()
    if soup.find('a', class_='developer'):
        developer = soup.find('a', class_='developer').text.strip()
    elif soup.find('p', class_='ver_dev'):
        developer = soup.find('p', class_='ver_dev').find('a').text.strip()
    date = None
    if soup.find('div', class_='date'):
        date = soup.find('div', class_='date').text.strip().lower()
    versions = []
    if soup.find('li', class_='version'):
        for i in soup.find_all('li', class_='version'):
            url = 'https://apkpure.net/' + i.find('a', class_='download-btn')['href']
            version = i.find('div', class_='code-info').find('span', class_='name').text.strip().lower()
            version_code = i.find('div', class_='code-info').find('span', class_='code').text.strip().lower().replace('(', '').replace(')', '')
            type = i.find('div', class_='code-info').find('span', class_='tag').text.strip().lower()
            t = i.find('div', class_='additional-info').find_all('span')
            date = t[0].text.strip().lower()
            size = t[1].text.strip().lower()
            android_version = t[2].text.strip().lower()
            versions.append({
                'url': url,
                'version': version,
                'version_code': version_code,
                'date': date,
                'size': size,
                'android_version': android_version
            })
    elif soup.find('a', class_='ver_download_link'):
        for i in soup.find_all('a', class_='ver_download_link'):
            version = i.find('div', class_='ver-item-n').text.strip().split('\n')[1].strip().lower()
            size = i.find('span', class_='ver-item-s').text.strip().lower()
            date = i.find('span', class_='update-on').text.strip().lower()
            url = i['href'].replace('/download/', '/downloading/')
            versions.append({
                'url': url,
                'version': version,
                'size': size,
                'date': date
            })
    return {
        'versions': versions,
        'title': title,
        'type': type,
        'developer': developer,
        'date': date
    }

def generate_download_url(version_url):
    r = requests.get(version_url)
    soop = bs4.BeautifulSoup(r.text, 'html.parser')
    download_url = None
    if soop.find('a', class_='download-start-btn'):
        download_url = soop.find('a', class_='download-start-btn')['href']
    elif soop.find('a', id='download_link'):
        download_url = soop.find('a', id='download_link')['href']
    type = 'xapk' if 'xapk' in download_url.lower() else 'apk'
    return {
        'download_url': download_url,
        'file_type': type
    }

def download(version_url, path_or_file_like, auto_file_extension=True):
    file = None
    download_info = generate_download_url(version_url)
    if isinstance(path_or_file_like, str):
        if auto_file_extension:
            path_or_file_like += '.' + download_info['file_type']
        file = open(path_or_file_like, 'wb')
    else:
        file = path_or_file_like
    r = requests.get(download_info['download_url'])
    file.write(r.content)
    file.close()