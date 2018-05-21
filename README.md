# Python-Github-Crawler
A Python Github crawler for reasearch pruposes. Search criteria can be set in a config file. The script can produce a list of found projects, clone those projects or saved them as zip files.

## Setup
- **python**
- **github token**: [How to create a token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) (it is possible to use the github API without token, but with token it is more flexible)
- for cloning repositories you need **GitPython** (not implemented yet): `pip install gitpython`

## Configuration
Crawler parameter:
- **user**: your user name
- **token**: your personal created token
- **make_repo_list**: should all found projects be saved in a txt file in the format "user_name/project_name" (true) or only printed out in the console (false)?
- **output_file**: path to the output file for project names
- **do_clone**: should projects be cloned with git on harddrive (true) or not (false) (todo)
- **do_zip**: should current project state be saved as zip on harddrive (true) or not (false)

Github Search Parameter:
- **created**: creation date of the project (e.g. `>2015-01-01`)
- **pushed**: date of last commit (e.g. `>2017-01-01`)
- **fork**:  should the project be forked from another one? (e.g. `false`) //todo
- **forks**:  how many forks should the project have (e.g. `>5`) //todo
- **search_query**:  after which names should be searched (e.g. `java swing`) //todo
- **search_location**:  where should be searched (e.g. `description`) //todo
- **language**:  what project languages should be included (e.g. `java`)
- **license**:  which [licence](https://help.github.com/articles/licensing-a-repository/) should the project have?
- **stars**:  how many stars should the projects have?  (e.g. `>100`)
- **topics**:  which tags should the project have?  (e.g. `parser`)
- **archived**:  should the project be archieved?  (e.g. `false`)

## Run
`python crawler.py crawler.conf`

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
- [x] implement project name output in txt file
- [ ] implement git clone for projects
- [ ] impement fetching projects as zip
- [ ] implement all possible search criteria

## References
- I used some parts of my script from [filter-github-projects](https://github.com/xai/filter-github-projects).
