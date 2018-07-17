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
	sleep(0.5)

get_pmt_cmd = "\
var hs = document.getElementsByClassName('feed-description__notes__headline');\
var ds = document.getElementsByClassName('feed-description__notes__meta');\
var ts = document.getElementsByClassName('feed-description__notes__content');\
var b = [];\
for (var i = 0; i < hs.length; i++) {\
	var h = hs[i].getElementsByTagName('span')[0];\
	var as = h.getElementsByTagName('a');\
	var n1 = as[0].getElementsByTagName('strong')[0].innerHTML;\
	var n2 = as[1].getElementsByTagName('strong')[0].innerHTML;\
	var dir = h.getElementsByTagName('span')[0].innerHTML;\
	if (dir.indexOf('paid') >= 0) {\
		dir = 'paid';\
	}\
	else if (dir.indexOf('charged') >= 0) {\
		dir = 'charged';\
	}\
	var date = ds[i].getElementsByTagName('span')[0].innerHTML;\
	var text = ts[i].getElementsByTagName('p')[0].innerHTML;\
	text = text.substring(text.indexOf('>')+1, text.length);\
	text = text.substring(0, text.indexOf('<'));\
	b.push([n1, n2, dir, date, text]);\
}\
return b;\
"
pmts = driver.execute_script(get_pmt_cmd)

f = open('payments_expanded.txt', 'w')
for pmt in pmts:
	terms = [str(p) for p in pmt]
	terms[-1] = '"' + terms[-1] + '"'
	f.write(','.join(terms) + '\n')

f.close()
driver.close()
