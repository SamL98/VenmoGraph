""" 
From the saved URLs of all friends in my timeline,
go to their profile and scrape all of their payments.
"""

from get_fr_pmts import get_pmts
from venmo_login import login

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start', type=str, dest='start', default=None)
args = parser.parse_args()

driver = login()

urls = []
with open('friend_urls.txt') as f:
	urls = f.read().split('\t')

if not args.start is None:
    urls = urls[urls.index('https://venmo.com/'+args.start):]

i = 0
for url in urls:
    if i % 10 == 0:
        print('\n%d / %d\n' % (i, len(urls)))
    get_pmts(url, driver)
    i += 1

driver.close()