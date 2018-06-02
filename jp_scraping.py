#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 22:02:50 2018

@author: xingyichong
"""
from bs4 import BeautifulSoup as BS
import requests
from collections import defaultdict

CAREER_URL = 'http://jobs.jpmorganchase.com/ListJobs/All/search/state/ny/country/us/city/new-york/sortdesc-postedon/page-'

def singlepage_career(page_count = 1):
    '''
    The generetor to grab the jost date & job name for single page
    '''
    response = requests.get(CAREER_URL + str(page_count))
    soup = BS(response.content, 'html.parser')
    
    soup_job_date = soup.find_all('td', {'class':'colpostedon'})
    soup_job_name = soup.find_all('td', {'class':'coldisplayjobid'})
    
    assert len(soup_job_name) == len(soup_job_date)
    
    for date, name in zip(soup_job_date, soup_job_name):
        yield name.find('a').get('href').split('/')[4], date.text[2:].strip()
 
def multipages_career(page_end, page_start = 1):    
    for page in range(page_start, page_end + 1):
        for element in singlepage_career(page):
            yield element



def dayjobcount(iterzip):
    '''
    Counting the total number of item in the first item(Job) of input iterator group by the second item(Date).
    '''
    count = defaultdict(int)
    for _, date in iterzip:
        count[date] += 1
    return count


if __name__ == "__main__":
    N = 8
   
    for i, (date, name) in enumerate(multipages_career(N)):
        print('({0}) {1}:  {2}'.format(i+1, name, date))
    # print the entire results, job name + post date
    
    dayjobdict = dayjobcount(multipages_career(N))
    # count the number of total job for each day
    
    for name, date in multipages_career(N):
        if date == '5-30-2018':
            print(name)
    # print all the job posted on the specific date


