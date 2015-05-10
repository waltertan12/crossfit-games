import requests, bs4, openpyxl, re, sqlite3

baseURL = 'http://games.crossfit.com/athlete/'
wb = openpyxl.load_workbook('cf1.xlsx',data_only=True)
sheet = wb.get_sheet_by_name('Sheet1')

excelIndex = int(sheet['B1'].value) + 1
excelStart = int(sheet['A' + str(excelIndex -1 )].value)

col = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q']

for x in range(excelStart+1,700000):
	# Download page
	res = requests.get(baseURL + str(x))
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text)

	# Regular expression to parse text from <dd></dd>
	regDD = re.compile(r'<dd>(.*)</dd>')

	# Regular expression to parse text from <td></td>
	regTD = re.compile(r'<td>(.*)</td>')

	# Continue only if athlete is found
	if str(soup.select('#page-title')).find(r'Not found') < 0:
		print("Scraping " + baseURL + str(x))
		last = len(soup.select('dd'))

		# Fill ID number
		sheet['A' + str(excelIndex)] = x

		# Fill Gender
		if str(soup.select('dd')).find('Female') < 0:
			sheet['B' + str(excelIndex)] = 'Female'

		else:
			sheet['B' + str(excelIndex)] = 'Male'

		# Fill age
		# sheet['C' + str(excelIndex)] = int(str(soup.select('dd')[last-3])[4:len(str(soup.select('dd')[last-3])[4:])-1])

		# Fill height
		# sheet['D' + str(excelIndex)] = str(soup.select('dd')[last-2])[4:len(str(soup.select('dd')[last-2])[4:])-1]

		# Fill weight
		weight = regDD.search(str(soup.select('dd')[last-1]))
		if weight.find("lb") > 0:
			# Weight is already in pounds, insert to db
			sheet('E' + str(excelIndex)) = int(weight[:len(weight)-3])
		else:
			# Convert weight from kilograms to pounds
			sheet('E' + str(excelIndex)) = int(weight[:len(weight)-3]) * 2.204
		# sheet['E' + str(excelIndex)] = str(soup.select('dd')[last-1])[4:len(str(soup.select('dd')[last-1])[4:])-1]

		# Fill workout data
		i = 1
		c = 5
		while i <= 23:
			sheet[col[c] + str(excelIndex)] = str(soup.select('td')[i])[4:len(str(soup.select('td')[i])[4:])-1]
			c += 1
			i += 2


		# Next row on Excel sheet
		excelIndex += 1

	else:
		print('Athlete ' + str(x) + ' not found')

	if x%25 == 0:
			wb.save('cf.xlsx')

def parseRank():
	# Ranking URL
	url1 = "http://games.crossfit.com/scores/leaderboard.php?stage=0&sort=0&page="
	url2 = "&division=1&region=0&numberperpage=100&competition=0&frontpage=0&expanded=0&year=15&full=0&showtoggles=1&hidedropdowns=1&showathleteac=0&=&is_mobile=&scaled=0&fittest=1&fitSelect=0"
	pageNumber = 1

	# Full URL
	url = url1 + str(pageNumber) + url2

	print(url)



def parseAthleteStats(athlete):
	# Athlete URL
	url = 'http://games.crossfit.com/athlete/' + str(athlete)

	# Download individual page
	res = requests.get(baseURL + str(x))
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text)

	# Regular expression to parse text from <dd></dd>
	regDD = re.compile(r'<dd>(.*)</dd>')

	# Regular expression to parse text from <td></td>
	regTD = re.compile(r'<td>(.*)</td>')