import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_titles_filtered = []
companies_names_filtered = []
location_filtered = []
job_type_filtered = []
job_skills_filtered = []
links = []
salary = []
publishing_date = []
job_requirements = []
page_number=0
while True :
    src=requests.get(f'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_number}').content
    soup=BeautifulSoup(src,'lxml')

    #parameters :)
    job_titles=soup.find_all('h2', {'class': 'css-m604qf'})
    companies_names=soup.find_all('a',{'class':'css-17s97q8'})
    location=soup.find_all('span',{'class':'css-5wys0k'})
    job_type=soup.find_all('div',{'class':'css-1lh32fc'})
    job_skills=soup.find_all('div', {'class': 'css-y4udm8'})

    for i in range(len(job_titles)):
        job_titles_filtered.append(job_titles[i].text)
        companies_names_filtered.append(companies_names[i].text)
        location_filtered.append(location[i].text)
        job_type_filtered.append(job_type[i].text)
        job_skills_filtered.append(job_skills[i].text)
        links.append(job_titles[i].find('a').attrs['href'])
    maxpage=int(soup.find('strong').text)//15
    page_number+=1
    if (page_number>maxpage):
        break
    print(f'Page {page_number} complete')

#----------------------------------------------------------------------
for link in links:
    src=requests.get('https://wuzzuf.net'+link).content
    soup=BeautifulSoup(src,'lxml')
    publishing_date.append(soup.find('span', {'class': 'css-182mrdn'}).text)
    job_requirements.append(soup.find('div',{'class':'css-1t5f0fr'}).text)
    print('done:)')
file_list=[job_titles_filtered,companies_names_filtered,location_filtered,publishing_date,job_type_filtered,links,job_skills_filtered,job_requirements]
exported=zip_longest(*file_list)
with open('G:\Courses\ML\In Queue\Python Projects\JobScraping_PythonDeveloper_WUZZUF.csv','w') as myfile:
    wr=csv.writer(myfile)
    wr.writerow(['Job Title','Company Name','Location','Publishing Date','Job Type','links','Skills','Job Requirements'])
    wr.writerows(exported)
