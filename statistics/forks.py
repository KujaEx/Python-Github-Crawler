"""
Count projects with specific forks count
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

def build_query_for_forks_number(forks_min, forks_max, per_page):
    query = ''
    """Call API"""
    query += 'https://api.github.com/search/'
    """Searching (default: repositories)"""
    query += 'repositories?q='

    """Forks criteria"""
    query += 'forks:' + str(forks_min) + '..' + str(forks_max)

    """Sorting, Order and Iteration Criteria"""
    query += '&sort=forks&order=desc&per_page=' + str(per_page) + '&page=1'

    return query

def count_projects():
    out = open(forks_output, 'a')
    i = forks_min 

    #mode 0: make for every fork count a request
    #mode 1: count in steps of fork_range (same output, different request handeling)
    mode = 0

    while True:
        if i <= forks_max:
            if mode == 0:
                """Make request with incrementing forks count"""
                url = build_query_for_forks_number(i,i,1)
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

                if i % forks_range == 0:
                    """ Maybe change mode? """
                    sleep(2)
                    print('check mode...')
                    url = build_query_for_forks_number(i,i+forks_range,1)
                    response = query(url)
                    result = json.loads(response.content.decode('utf-8'))
                    if int(result['total_count']) < 900:
                        mode = 1
                        print('changed mode to ' + str(forks_range) + ' steps in forks count')
                    else:
                        print('mode stays on each forks count')



            if mode == 1:
                forksList = [0] * forks_range

                url = build_query_for_forks_number(i,i+forks_range,100)
                response = query(url)
                result = json.loads(response.content.decode('utf-8'))


                while True:
                    """Wait for API, 30 requests per minute (sleep 2sec per request)"""
                    sleep(wait)

                    """Loop over result pages until there is no 'next page' link."""
                    for repo in result['items']:
                        if int(repo['forks_count']) in range(i,i+100):
                            forksList[int(repo['forks_count'])-i-1] += 1

                    if 'next' in response.links:
                        url = response.links['next']['url']
                        response = query(url)
                        result = json.loads(response.content.decode('utf-8'))
                    else:
                        break

                """Save statistics"""
                for j in range(forks_range):
                    if forksList[j] > 0:
                        out.write(str(i+j) + ',' + str(forksList[j]) + '\n')
                        out.flush()

                i += forks_range

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
    global forks_output
    global forks_min
    global forks_max
    global forks_range

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
    forks_min = int(config['forks']['forks_min'])
    forks_max = int(config['forks']['forks_max'])
    forks_output = config['forks']['forks_output']
    forks_range = 100

    count_projects()