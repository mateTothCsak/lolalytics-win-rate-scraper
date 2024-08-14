# lolalytics-win-rate-scraper

Hi all,

I am working on a pet project which requires collecting the most played League of Legends champions' win data for each lane... against and with all other champions on each lane.

https://lolalytics.com is a very good source for this kind of information, so it will be used as the base.

Depending on the export size, I might upload the scraping results as Json objects for easier access.


### Requirements
This section will be uploaded later on but as WIP notes, you will need:
    - python 3
    - selenium
    - a chrome driver from selenium


Since this is a one-person project I don't bother too much with branching etc, all straight to master B)


Example model for an outcome of a champion comparison:
```
{
    "champion_name": "Aatrox",
    "champion_role": "Top",
    "partner_champion_name": "Yuumi",
    "partner_role": "Support",
    "win_rate_with": 0.52,
    "pick_rate_with": 0.03,
    "games_with": 505,
    "win_rate_against": 0.47,
    "pick_rate_against": 0.02,
    "games_against": 403
}
```
where the fields ending "with" represent when the two champions played on the same team, and "against" the cases when they were opponents.

In this example, in games where Aatrox Top played with Yuumi Support in the same team they had a win rate of 52%, when Aatrox Top was in one team and Yuumi Support was on the oter Aatrox had only a win rate of 47%.
