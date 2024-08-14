import json

class ChampionSynergyStats:
        
    def __init__(self, champion_name, champion_role, partner_champion_name, 
                 partner_role, win_rate_with=None, pick_rate_with=None, 
                 games_with=None, win_rate_against=None, pick_rate_against=None, 
                 games_against=None):
        self.champion_name = champion_name
        self.champion_role = champion_role
        self.partner_champion_name = partner_champion_name
        self.partner_role = partner_role
        self.win_rate_with = win_rate_with
        self.pick_rate_with = pick_rate_with
        self.games_with = games_with
        self.win_rate_against = win_rate_against
        self.pick_rate_against = pick_rate_against
        self.games_against = games_against

    def __str__(self):
        # Create a dictionary of all the instance attributes
        data = {
            "champion_name": self.champion_name,
            "champion_role": self.champion_role,
            "partner_champion_name": self.partner_champion_name,
            "partner_role": self.partner_role,
            "win_rate_with": self.win_rate_with,
            "pick_rate_with": self.pick_rate_with,
            "games_with": self.games_with,
            "win_rate_against": self.win_rate_against,
            "pick_rate_against": self.pick_rate_against,
            "games_against": self.games_against
        }
        # Convert dictionary to JSON string
        return json.dumps(data, indent=4)
