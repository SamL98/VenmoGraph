from time import sleep
from venmo_login import login

driver = login()

num_pmt_cmd = "return document.getElementsByClassName('feed-story-payment').length;"
more_pmt_cmd = "document.querySelector('#activity-feed > div > div:nth-child(2) > div.feed-more > button').click();"

prev_num_pmt = 0
num_pmt = driver.execute_script(num_pmt_cmd)

while prev_num_pmt < num_pmt:
	if num_pmt == 780:
		break

	driver.execute_script(more_pmt_cmd)
	sleep(0.5)

	prev_num_pmt = num_pmt
	num_pmt = driver.execute_script(num_pmt_cmd)
	sleep(0.25)

print('Finished loading payments')

get_url_cmd = "\
var hs = document.getElementsByClassName('feed-description__notes__headline');\
var b = [];\
for (var i = 0; i < hs.length; i++) {\
	var h = hs[i].getElementsByTagName('span')[0];\
	var as = h.getElementsByTagName('a');\
	b.push(as[0].getAttribute('href'));\
	b.push(as[1].getAttribute('href'));\
}\
return b;\
"
urls = driver.execute_script(get_url_cmd)
urls = list(set(urls))

f = open('friend_urls.txt', 'w')
f.write('\t'.join(urls))
f.close()
driver.close()
