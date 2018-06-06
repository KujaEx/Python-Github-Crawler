# Python-Github-Crawler
A Python Github crawler for reasearch pruposes. Search criteria can be set in a config file. The script can produce a list of found projects, clone those projects or saved them as zip files.

## Setup
- **python**
- **github token**: [How to create a token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) (it is possible to use the github API without token, but with token it is more flexible)
- some python packages need to be installed: (e.g. simply by `pip install package-name`)
	- requests (for api and download requests)
	- configparser (for reading config file)
	- gitpython (to clone repositories)
	- tqdm (to show progress bar when download repository

## Configuration
Crawler parameter:
- **user**: your github user name
- **token**: your personal created token
- **make_repo_list**: should all found projects be saved in a txt file in the format "user_name/project_name" (true) or only printed out in the console (false)?
- **list_output**: path to the output file for project names
- **do_clone**: should projects be cloned with git on harddrive (true) or not (false)
- **clone_output**: path to the directory where the projects have to be cloned
- **do_zip**: should current project state be saved as zip on harddrive (true) or not (false) - **zip_output**: path to the directory where the projects are downloaded
- **count**: how many projects should be crawled?

Github Search Parameter:
- **created**: creation date of the project (e.g. `>2015-01-01`)
- **pushed**: date of last commit (e.g. `>2017-01-01`)
- **fork**: should the project be forked from another one? (e.g. `false` or `only`)
- **forks**: how many forks should the project have? (e.g. `>5`)
- **search_query**: after which tags should be searched? (e.g. `swing`) //todo
- **search_location**: should be searched in name, description or readme? (e.g. `description`) //todo
- **language**: what project languages should be included (e.g. `java`)
- **license**: which [licence](https://help.github.com/articles/licensing-a-repository/) should the project have? //todo
- **stars**: how many stars should the projects have?  (e.g. `>100`)
- **topic**: which tag should the project have?  (e.g. `parser`)
- **topics**: how many tags should the project have?  (e.g. `>=2`)
- **archived**: should the project be archieved?  (e.g. `false`)

You have to use your github user name and your own personal token. If the other parameters are empty in the config file, they won't be considered in the search. Possible values for queries of numbers (e.g. `100`) are: equal `100`, less `<100`, less equal `<=100`, greater `>100`, greater equal `>=100`, range `10..100`, unclosed range `100..*`. The same operators are usable with dates in the form of `YYYY-MM-DD`.
More about [possible values for search parameters](https://help.github.com/articles/searching-repositories/) and the [search for repositories](https://developer.github.com/v3/search/#search-repositories).

## Run
`python crawler.py -c crawler.conf`

If you don't give the path to the config file as parameter, the program assumes that the `crawler.conf` file is in the same folder. You can use the config file in this repository as an example. Complete it with your own user, token and search criteria information.

## Output
The output can be a text list with all found repositories (in the form "user/project-name"), the cloned projects (todo) or the projects in their current state as zip file (todo).

Example output:
```
iluwatar/java-design-patterns
ReactiveX/RxJava
elastic/elasticsearch
square/retrofit
...
```

## TODO
- [x] use parameters for search in github api (read from config file)
- [x] implement project name output in console or text file
- [x] implement git clone for projects
- [x] impement downloading projects as zip
- [x] implement search criteria (not tested)
- [x] create statistics for project distributions (on the basis of stars, forks etc.)

## References
- I used some parts of my script from [filter-github-projects](https://github.com/xai/filter-github-projects).
- [Script for progress bar](https://stackoverflow.com/a/10744565/2520160) when downloading zips of projects
