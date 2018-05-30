In this folder are small scripts which use the github API to create statistics about specific parameters, e.g. number of stars, forks or issues.

The crawler for searching projects works in two different modes:
- mode 0: the crawler requests all projects e.g. with "1 star" and saves the total number 
(advantage: counts many projects with one specific star fast; disadvantage: after e.g. "2000 star" the probability that there is even one project is pretty low -> many empty responses)
- mode 1: the crawler requests all projects in a range e.g. with "5000..5099 stars" and counts the projects in a range list to the specific range number
(advantage: counts few projects with high star numbers faster with ranges because of less requests; disadvantage: doesn't work when a range has over 1000 results because of API limit)

The crawler starts always with mode 0 and changes to mode 1 when there are less then 900 (api limit 1000 minus buffersize) results in a range.

The script assumes that there are less and less projects with higher star count and the mode doesn't change back from 1 to 0. If there are more projects with 1000 in a later range than in the one before (e.g. projectcount("5000..5099 stars") < projectcount("5100..5199 stars") > 1000) then only the first 1000 project search results are counted.
