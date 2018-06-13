"""
Count projects with specific star number
for research purposes on Github.

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

    """Stars criteria"""
    query += 'stars:' + str(stars_min) + '..' + str(stars_max)

    """Sorting, Order and Iteration Criteria"""
    query += '&sort=stars&order=desc&per_page=' + str(per_page) + '&page=1'

    return query

def count_projects():
    out = open(stars_output, 'a')
    i = stars_min 

    #mode 0: make for every star count a request
    #mode 1: count in steps of star_range (same output, different request handeling)
    mode = 0

    while True:
        if i <= stars_max:
            if mode == 0:
                """Make request with incrementing star count"""
                url = build_query_for_stars_number(i,i,1)
                response = query(url)
                result = json.loads(response.content.decode('utf-8'))

                """write statistics to output file if projects were found"""
                if int(result['total_count']) > 0:
                    out.write(str(i) + ',' + str(result['total_count']) + '\n')
                    out.flush()

                """Wait for API, 30 requests per minute (sleep 2sec per request)"""
                sleep(wait)

                """Increment and print progress"""
                i += 1

                if i % star_range == 0:
                    """ Maybe change mode? """
                    sleep(2)
                    print('check mode...')
                    url = build_query_for_stars_number(i,i+star_range,1)
                    response = query(url)
                    result = json.loads(response.content.decode('utf-8'))
                    if int(result['total_count']) < 900:
                        mode = 1
                        print('changed mode to ' + str(star_range) + ' steps in star count')
                    else:
                        print('mode stays on each star count')



            if mode == 1:
                starList = [0] * star_range

                url = build_query_for_stars_number(i,i+star_range,100)
                response = query(url)
                result = json.loads(response.content.decode('utf-8'))


                while True:
                    """Wait for API, 30 requests per minute (sleep 2sec per request)"""
                    sleep(wait)
                    
                    """Loop over result pages until there is no 'next page' link."""
                    for repo in result['items']:
                        starList[int(repo['stargazers_count'])-i-1] += 1

                    if 'next' in response.links:
                        url = response.links['next']['url']
                        response = query(url)
                        result = json.loads(response.content.decode('utf-8'))
                    else:
                        break

                """Save statistics"""
                for j in range(star_range):
                    if starList[j] > 0:
                        out.write(str(i+j) + ',' + str(starList[j]) + '\n')
                        out.flush()

                i += star_range

            """print progress"""
            if i % 100 == 0:
                    print(i)
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
    global star_range

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
    star_range = 100

    count_projects()