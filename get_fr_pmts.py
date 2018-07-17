"""
Get the payments of a given Venmo user given their username.
Technically, given their URL, but that's just http://venmo.com/username
"""

from time import sleep
from selenium.common.exceptions import NoSuchElementException

"""
Click the button on the user's profile to load more payments.

If the button is not found, return -1. 
Otherwise click the button and return 0.

:param driver: the Selenium webdriver to use
"""
def get_more_pmt(driver):
	try:
		button = driver.find_element_by_xpath('//*[@id="profile_feed_MORE_BUTTON"]/a')
	except NoSuchElementException:
		#print('more button is not in DOM')
		return -1
	
	button.click()
	return 0

"""
Scrape and format the payments on the user's profile.
Append the results to the payments file.

:param url: the url of the user's profile
:param driver: the Selenium webdriver to use
"""
def get_pmts(url, driver):
	username = url[url.rindex('/'):]

	# navigate to the url and let the page load
	driver.get(url)
	sleep(2)

	# the javascript to return the number of payments displayed
	num_pmt_cmd = "return document.getElementsByClassName('profile_feed_story').length;"

	prev_num_pmt = 0
	num_pmt = driver.execute_script(num_pmt_cmd)

	# keep pressing the 'load more' button until the amount of payments displayed
	# is the same as the previous number
	while prev_num_pmt < num_pmt:
		ret_code = get_more_pmt(driver)
		if ret_code < 0:
			break

		sleep(0.5)

		prev_num_pmt = num_pmt
		num_pmt = driver.execute_script(num_pmt_cmd)

		sleep(0.25)

	print('%s: %d payments counted' % (username[1:], num_pmt))

	get_pmt_cmd = "\
	var ps = document.getElementsByClassName('align_top p_ten_l p_ten_b');\
	var b = [];\
	for (var i = 0; i < ps.length; i++) {\
		var p = ps[i].getElementsByTagName('div')[0];\
		var ds = p.getElementsByTagName('div');\
		var ft = ds[0].innerText;\
		var as = ds[0].getElementsByTagName('a');\
		if (as.length < 2) {\
			continue;\
		}\
		var u1 = as[0].getAttribute('href');\
		var u2 = as[1].getAttribute('href');\
		var t = ds[1].innerText;\
		b.push([ft, u1, u2, t]);\
	}\
	return b;\
	"
	pmts = driver.execute_script(get_pmt_cmd)
	sleep(2)

	f = open('payments_expanded_fr.txt', 'a')
	for pmt in pmts:
		headline = pmt[0]
		if 'paid' in headline:
			i = headline.index('paid')
			d = 'paid'
		elif 'charged' in headline:
			i = headline.index('charged')
			d = 'charged'
		else:
			print('Poorly formatted headline: %s' % headline)
			continue

		n1 = headline[:i-1]
		n2 = headline[i+len(d)+1:]

		if pmt[1].lower() == username.lower():
			u = pmt[2]
		elif pmt[2].lower() == username.lower():
			u = pmt[1]
		else:
			print('Bad URLs (%s): %s, %s' % (username, pmt[1], pmt[2]))
			continue

		terms = [n1, n2, d, u, pmt[-1]]
		terms[-1] = '"' + terms[-1] + '"'
		f.write(','.join(terms) + '\n')

	f.close()
