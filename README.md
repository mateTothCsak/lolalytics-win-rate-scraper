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
    "champion_name": "aatrox",
    "champion_role": "top",
    "partner_champion_name": "yuumi",
    "partner_role": "support",
    "partner_relation": "enemy",
    "win_rate": 0.52,
    "pick_rate": 0.03,
    "number_of_games": 505
}
```


In this example, in games where Aatrox Top played against Yuumi Support in the enemy team they had a win rate of 52%, there were a total of 505 games, and Yuumi support was picked in 3% of games against Aatrox. (based on lolalytics data)
