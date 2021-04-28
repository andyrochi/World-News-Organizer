import subprocess,time
from newsapi import NewsApiClient
import functions

# Initialize
newsapi = NewsApiClient(api_key='b0ff9c340dbc4a1b8044435f6568e73b')

print('Welcome to News Organizer!')
time.sleep(1)
news_source = ['The New York Times','Times','Reuters','BBC News','The Wall Street Journal','The Associated Press','Al-Jazeera','CNN']

#show available sources for user to choose
print('The following news sources are available:')
index = 1
for source in news_source:
    print(str(index)+'.',source)
    index += 1

#prompt user for input
numbers = ['1','2','3','4','5','6','7','8']
print('You may choose three news sources to view.\nPlease enter your choices:(Input has to be 1~8)')
choices = list()

for number in range(1,4):
    choice = input('Choice '+str(number)+':')
    while choice not in numbers:
        choice = input('Wrong input format, please enter choice '+str(number)+' again:')
    choices.append(choice)
    numbers.remove(choice)

print('The sources that you have chosen are:')
for number in choices:
    key = int(number)
    print(number+'.', news_source[key-1])

f = open('page.html','w+')
f.write('<!DOCTYPE html>\n<html>\n')
f.write('<head><title>News Organizer!</title></head>\n<body>')

for choice in choices:
    print('Requesting data from:',news_source[int(choice)-1],'...')
    data = functions.get_news(newsapi,choice)
    i = 1
    print('Writing data...')
    for news in data:
        f.write('<h2>'+news['title']+'</h2>\n')
        if news['author'] != None:
            f.write('<p>'+'Source: ' + news['author']+'<br></p>\n')

        f.write('<img src="'+news['image']+'" height ="256" alt= "photo'+str(i)+'">\n')
        f.write('<p>'+'Description: '+news['description']+'</p>\n')
        f.write('<p>'+'Keywords: ')
        count = 0
        keywords = news['keywords']
        related = news['related']
        for keyword in keywords:
            keyword_string = '<span '+'title="'+related[keyword]+'">'+keyword+'</span>'
            f.write(keyword_string)
            count += 1
            if count >= 5 or count >= len(keywords):
                break
            else:
                f.write(' - ')
        
        f.write('</p>\n')
        f.write('<a href="'+news['url']+'">'+'Read more...'+'<br><br><br></a>\n')
        i += 1

f.write('</body>\n</html>')
f.close()

subprocess.run(['open', 'page.html'], check=True)