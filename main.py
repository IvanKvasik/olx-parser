import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import threading

search = input('Search query: ')

r = requests.get('https://www.olx.ua/d/uk/list/q-' + '-'.join(search.split()))

soup = BS(r.content, 'html.parser')
posts_l = [[], [], []]

posts = 0
def ParsePage(i):
	global posts, posts_l, search
	if(i==0):
		r = requests.get('https://www.olx.ua/d/uk/list/q-' + '-'.join(search.split()))
	else:
		r = requests.get('https://www.olx.ua/d/uk/list/q-' + '-'.join(search.split()) + '?page=' + str(i))
	soup = BS(r.content, 'html.parser')
	for post in soup.select('[data-cy="l-card"]'):
		posts_l[0].append(post.select('h6')[0].text)
		try:
			posts_l[1].append(post.select('.css-u2ayx9 > p')[0].text)
		except:
			posts_l[1].append('-')
		posts_l[2].append('https://www.olx.ua' + post.select('a')[0].get('href'))
		posts +=1
threads = []
for i in range(int(soup.select('.pagination-item')[-1].text)+1):
	threads.append(threading.Thread(target=ParsePage, args=[i]))
	threads[i].start()

for j in threads:
	j.join()

writer = pd.ExcelWriter('_'.join(search.split()) + '.xlsx')
xls = pd.DataFrame({'Name': posts_l[0], 'Cost': posts_l[1], 'Link': posts_l[2]})
xls.to_excel(writer, sheet_name=search, index=False)

for i in range(3):
	writer.sheets[search].column_dimensions[chr(65+i)].width = 50

writer.save()

print('Parsing ended. ' + str(posts) + ' results')
