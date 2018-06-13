"""
Crawls java projects with star count.
Saves meta data and crawls 100 per star at max.

author: Kevin Lang
e-mail: kevin.lang@uni-weimar.de
"""

import argparse
import requests
import json
import sys
import configparser
from time import sleep


def query(url):
    response = requests.get(url, auth=(user, token))

    if response.ok:
        return response
    else:
        response.raise_for_status()

def build_query_for_stars_number(stars_min, stars_max, per_page):
    query = ''
    """Call API"""
    query += 'https://api.github.com/search/'
    """Searching (default: repositories)"""
    query += 'repositories?q='

    """Language criteria"""
    query += 'language:java+'

    """Stars criteria"""
    query += 'stars:' + str(stars_min) + '..' + str(stars_max)

    """Sorting, Order and Iteration Criteria"""
    query += '&sort=stars&order=asc&per_page=' + str(per_page) + '&page=1'

    return query

def crawl_projects():
    out = open(stars_output, 'a')
    i = stars_min 

    #mode 0: make for every star count a request
    #mode 1: count in steps of star_range (same output, different request handeling)
    mode = 0

    while True:
        if i <= stars_max:
            print(i)
            """Make request with incrementing star count"""
            url = build_query_for_stars_number(i,i+star_ranges[mode]-1,100)
            response = query(url)
            result = json.loads(response.content.decode('utf-8'))
                
            """Loop over result pages until there is no 'next page' link."""
            for repo in result['items']:
                out.write(str(repo['stargazers_count']) + ',' + repo['full_name'] + ',' + str(repo) + '\n')
                out.flush()

            """Wait for API, 30 requests per minute (sleep 2sec per request)"""
            sleep(wait)

            """Increment and print progress"""
            i += star_ranges[mode]

            """ Maybe change mode? """
            if i % range_check == 0:
                sleep(wait)
                print('check mode...')
                url = build_query_for_stars_number(i,i+star_ranges[mode+1]-1,1)
                response = query(url)
                result = json.loads(response.content.decode('utf-8'))
                if int(result['total_count']) < 90:
                    mode += 1
                    print('changed mode to ' + str(star_ranges[mode]) + ' steps in star count')
        else:
            break

    out.close()
    print('Done!')

if __name__ == '__main__':

    global token
    global user
    global stars_output
    global stars_min
    global stars_max
    global star_ranges
    global wait

    """Get Config Path"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help='config file path',
                        default='crawler.conf',
                        type=str)
    args = parser.parse_args()

    """Get Config Parameters"""
    config = configparser.ConfigParser()
    config.read(args.config)

    token = config['crawler']['token']
    user = config['crawler']['user']
    wait = float(config['crawler']['wait'])
    stars_min = int(config['stars']['stars_min'])
    stars_max = int(config['stars']['stars_max'])
    stars_output = config['stars']['stars_output']
    range_check = 100
    star_ranges = [1,5,10,20,50,100,500,1000,10000,100000,1000000,10000000,100000000,1000000000]

    crawl_projects()