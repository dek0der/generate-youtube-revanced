#!/usr/bin/python

import requests, json, os
from bs4 import BeautifulSoup

base_url = 'https://github.com'
revanced_cli_url = 'https://github.com/ReVanced/revanced-cli/releases/latest'
revanced_patches_url = 'https://github.com/ReVanced/revanced-patches/releases/latest'
revanced_integrations_url = 'https://github.com/ReVanced/revanced-integrations/releases/latest'

revanced_files_url = [revanced_cli_url, revanced_integrations_url, revanced_patches_url]


def find_latest_version(url):
    retry_count = 5
    temp_package_name = url.split('/')[4]
    package_name = ''
    if temp_package_name == 'revanced-cli':
        package_name = 'ReVanced CLI'
    elif temp_package_name == 'revanced-patches':
        package_name = 'ReVanced Patches'
    elif temp_package_name == 'revanced-integrations':
        package_name = 'ReVanced Integrations'

    for i in range(retry_count):
        try:
            page = requests.get(url)
            if page.status_code == 200:
                break
        except:
            print('[+] An error occurred')
            print('[+] Retrying ' + str(i + 1) + ' of ' + str(retry_count))
    soup = BeautifulSoup(page.content, 'lxml')
    assets = soup.find_all('include-fragment', {'loading' : 'lazy'})
    latest_version_page = assets[0]['src']
    print('[+] Latest version of ' + package_name + ' is: ' + latest_version_page.split('/')[-1])
    return latest_version_page

def find_latest_version_file_url(url, base_url, index):
    retry_count = 5
    for i in range(retry_count):
        try:
            page = requests.get(url)
            if page.status_code == 200:
                break
        except:
            print('[+] An error occurred')
            print('[+] Retrying ' + str(i + 1) + ' of ' + str(retry_count))
    soup = BeautifulSoup(page.content, 'lxml')
    links = soup.find_all('a', {'class' : 'Truncate'})
    latest_download_link = base_url + links[index]['href']
    return latest_download_link

def download_file(url):
    retry_count = 5
    filename = url.split('/')[-1]
    print('[+] Downloading ' + filename)
    for i in range(retry_count):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                break
        except:
            print('[+] An error occurred')
            print('[+] Retrying ' + str(i + 1) + ' of ' + str(retry_count))
    with open(filename, mode="wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            file.write(chunk)
    print('[+] Download completed successfully')
    print('')
    return filename

def find_latest_supported_youtube_ver(url):
    index = 0
    retry_count = 5
    latest_version_page_url = find_latest_version(url)
    download_link = find_latest_version_file_url(latest_version_page_url, base_url, index)
    print('[+] Finding latest supported version of YouTube for ReVanced in ' + download_link.split('/')[-1])
    for i in range(retry_count):
        try:
            response = requests.get(download_link)
            if response.status_code == 200:
                break
        except:
            print('[+] An error occurred')
            print('[+] Retrying ' + str(i + 1) + ' of ' + str(retry_count))
    json_str = json.loads(response.content)
    latest_ver = json_str[0]['compatiblePackages'][0]['versions'][-1]
    print('[+] Latest supported version of YouTube for ReVanced is v' + latest_ver)
    return latest_ver

def get_latest_supported_youtube_ver(yt_version):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    headers = {'User-Agent' : user_agent}
    yt_version = yt_version.replace('.', '-')
    apkmirror_url = 'https://www.apkmirror.com'
    apkmirror_yt_url = 'https://www.apkmirror.com/apk/google-inc/youtube/youtube-' + yt_version + '-release/'
    package_base_name = 'com.google.android.youtube_'
    package_name = package_base_name + yt_version.replace('-', '.') + '.apk'

    print('[+] Searching for YouTube v' + yt_version.replace('-', '.') + ' on APKMirror')
    print('[+] Opening webpage ' + apkmirror_yt_url)

    retry_count = 5
    for i in range(retry_count):
        try:
            response = requests.get(apkmirror_yt_url, headers=headers)
            if response.status_code == 200:
                break
        except:
            print('[+] An error occurred')
            print('[+] Retrying ' + str(i + 1) + ' of ' + str(retry_count))
    soup = BeautifulSoup(response.content, 'lxml')
    yt_links =  soup.find_all('div', attrs={'class' : 'table-row headerFont'})
    yt_apk_page = apkmirror_url
    for i in range(1, len(yt_links)):
        if yt_links[i].find_all('span', attrs={'class' : 'apkm-badge'})[0].text == 'APK':
            yt_apk_page = yt_apk_page + yt_links[i].find_all('a', attrs={'class' : 'accent_color'})[0]['href']

    print('[+] Searching for YouTube v' + yt_version.replace('-', '.') + ' APK download page')

    for i in range(retry_count):
        try:
            res = requests.get(yt_apk_page, headers=headers)
            if res.status_code == 200:
                break
        except:
            print('[+] An error occurred')
            print('[+] Retrying ' + str(i + 1) + ' of ' + str(retry_count))
    soup = BeautifulSoup(res.content, 'lxml')
    apk_dl_page = soup.find_all('a', attrs={'class' : 'accent_bg'})
    apk_dl_page_url = apkmirror_url + apk_dl_page[0]['href']

    print('[+] Found webpage ' + apk_dl_page_url)
    print('[+] Opening webpage ' + apk_dl_page_url)
    print('[+] Searching for YouTube v' + yt_version.replace('-', '.') + ' APK download link')

    for i in range(retry_count):
        try:
            res = requests.get(apk_dl_page_url, headers=headers)
            if res.status_code == 200:
                break
        except:
            print('[+] An error occurred')
            print('[+] Retrying ' + str(i + 1) + ' of ' + str(retry_count))
    soup = BeautifulSoup(res.content, 'lxml')
    apk_page_details = soup.find_all('a', attrs={'rel' : 'nofollow'})
    apk_link = apkmirror_url + apk_page_details[0]['href']

    print('[+] Found download link ' + apk_link)
    print('[+] Downloading and saving to ' + package_name)

    for i in range(retry_count):
        try:
            apk_file = requests.get(apk_link, headers=headers, stream=True)
            if apk_file.status_code == 200:
                break
        except:
            print('[+] An error occurred')
            print('[+] Retrying ' + str(i + 1) + ' of ' + str(retry_count))
    with open(package_name, mode='wb') as file:
        for chunk in apk_file.iter_content(chunk_size=1024 * 1024):
            file.write(chunk)
    
    print('[+] Download completed successfully')
    return package_name

def generate_command(file_names):
    with open('generate-revanced-apk.bat', 'w') as file:
        file.write('java -jar ' + file_names[0] + ' patch -b ' + file_names[2] + ' -o YouTube-ReVanced-' + file_names[4] + '.apk ' + ' -m ' + file_names[1] + ' ' + file_names[3] )


filenames = []

for url in revanced_files_url:
    index = 0
    if 'patches' in url:
        index = 1
    latest_version_page_url = find_latest_version(url)
    download_link = find_latest_version_file_url(latest_version_page_url, base_url, index)
    filenames.append(download_file(download_link))


yt_version = find_latest_supported_youtube_ver(revanced_files_url[2])

filenames.append(get_latest_supported_youtube_ver(yt_version))
filenames.append(yt_version)

print('[+] Creating batch file generate-revanced-apk.bat')
generate_command(filenames)
print('[+] Executing script "generate-revanced-apk.bat"')
os.system("generate-revanced-apk.bat")
