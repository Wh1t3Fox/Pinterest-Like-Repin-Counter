#!/usr/bin/env python

import time
import argparse
import requests
from multiprocessing import Process
from bs4 import BeautifulSoup as bs

repins = 0
likes = 0

def thread_handler(link):
    global repins
    global likes

    r = requests.get(link)
    soup = bs(r.text)

    like_em = soup.find_all('em', {'class' : 'likeCountSmall'})
    repin_em = soup.find_all('em', {'class' : 'repinCountSmall'})

    if like_em:
        for entry in like_em:
            likes += int(entry.get_text().strip())

    if repin_em:
        for entry in repin_em:
            repins += int(entry.get_text().strip())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find the number of likes and repins of a Pinterest user')
    parser.add_argument('-u', '--username', required=True, help='Pinterest username')
    args = parser.parse_args()

    username = args.username
    url = "http://www.pinterest.com/{}/".format(username)
    ignore = ['boards', 'pins', 'likes', 'followers', 'following']

    try:
        r = requests.get(url)
        soup = bs(r.text)

        for links in soup.find_all('a'):
            suffix = links.get('href')
            if username in suffix and suffix[11:-1] not in ignore:
                link = 'http://www.pinterest.com' + suffix
                p = Process(target=thread_handler, args=(link,))
                p.start()
                p.join()

        time.sleep(2)
        print("Likes: {}".format(likes))
        print("Repins: {}".format(repins))

    except Exception as e:
        print(str(e))
