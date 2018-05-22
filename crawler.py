"""
Find projects for research purposes on Github.

The goal is to filter the list of projects found
by criteria like minimum number or issues or pull requests.

author: Kevin Lang
e-mail: kevin.lang@uni-weimar.de
"""

import argparse
import requests
import json
import re
import sys
import configparser
from distutils.util import strtobool


def query(url):
    response = requests.get(url, auth=(user, token))

    if response.ok:
        return response
    else:
        response.raise_for_status()

def build_query():
    query = ""
    """Call API"""
    query += 'https://api.github.com/search/'
    """Searching (default: repositories)"""
    query += 'repositories?q='

    """Stars criteria"""
    if len(stars) > 0:
        query += 'stars:' + stars + '+'
    """Creation date criteria"""
    if len(created) > 0:
        query += 'created:' + created + '+'
    """Pushed date criteria"""
    if len(pushed) > 0:
        query += 'pushed:' + pushed + '+'
    """Fork criteria"""
    if len(fork) > 0:
        query += 'fork:' + fork + '+'
    """Forks criteria"""
    if len(forks) > 0:
        query += 'forks:' + forks + '+'
    """Search_in criteria"""
    if len(search_in) > 0:
        query += 'in:' + search_in + '+'
    """Language criteria"""
    if len(language) > 0:
        query += 'language:' + language + '+'
    """Topic criteria"""
    if len(topic) > 0:
        query += 'topic:' + topic + '+'
    """Topics criteria"""
    if len(topics) > 0:
        query += 'topics:' + topics + '+'
    """Archived criteria"""
    if len(archived) > 0:
        query += 'archived:' + archived + '+'
    """License criteria"""
    if len(license) > 0:
        query += 'license:' + license + '+'

    """Sorting, Order and Iteration Criteria"""
    if query.endswith('+'):
        query = query[:-1]
    query += '&sort=stars&order=desc&per_page=1000&page=1'

    return query

def find_projects():
    url = build_query()

    response = query(url)
    result = json.loads(response.content.decode('utf-8'))

    if make_repo_list and output_file:
        out = open(output_file, 'w')

    i = 0

    print('total number of projects: ' + str(result['total_count']))
    print('crawling projects: ' + str(min(count,int(result['total_count']))))

    while True:
        """Loop over result pages until there is no 'next page' link."""
        for repo in result['items']:
            if i < count:
                i += 1
                """Save user and repo name as identifier"""
                if make_repo_list and output_file:
                    out.write(repo['full_name'] + '\n')
                else:
                    print(repo['full_name'])
                    sys.stdout.flush()

                """Clone repo"""
                if do_clone:
                    # TODO: clone repo
                    print('TODO: Clone repository "' + repo['full_name'] + '"')

                """Save zip file of repo"""
                if do_zip:
                    # TODO: save zip of repo
                    print('TODO: Download repository as zip "' + repo['full_name'] + '"')

                if i % 100 == 0:
                    print(i)



        if 'next' in response.links and i < count:
            url = response.links['next']['url']
            response = query(url)
            result = json.loads(response.content.decode('utf-8'))
        else:
            break

    if make_repo_list and output_file:
        out.close()

if __name__ == "__main__":

    global token
    global user
    global repo_list
    global do_clone
    global do_zip
    global output_file
    global count

    global created
    global pushed
    global fork
    global forks
    global search_in
    global language
    global license
    global stars
    global topic
    global topics
    global archived

    """Get Config Path"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        help="config file path",
                        default='crawler.conf',
                        type=str)
    args = parser.parse_args()

    """Get Config Parameters"""
    config = configparser.ConfigParser()
    config.read(args.config)

    token = config['crawler']['token']
    user = config['crawler']['user']
    make_repo_list = bool(strtobool(config['crawler']['make_repo_list']))
    output_file = config['crawler']['output_file']
    do_clone = bool(strtobool(config['crawler']['do_clone']))
    do_zip = bool(strtobool(config['crawler']['do_zip']))
    count = int(config['crawler']['count'])

    created = config['github']['created']
    pushed = config['github']['pushed']
    fork = config['github']['fork']
    forks = config['github']['forks']
    search_in = config['github']['search_in']
    language = config['github']['language']
    license = config['github']['license']
    stars = config['github']['stars']
    topic = config['github']['topic']
    topics = config['github']['topics']
    archived = config['github']['archived']

    find_projects()