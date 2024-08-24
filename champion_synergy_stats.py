import json

class ChampionSynergyStats:
        
    def __init__(self, champion_name: str, champion_role: str, partner_champion_name: str, 
                 partner_role: str, partner_relation: str, win_rate: float, 
                 pick_rate : float, number_of_games: int):
        self.champion_name: str = champion_name
        self.champion_role: str = champion_role
        self.partner_champion_name: str = partner_champion_name
        self.partner_role: str = partner_role
        self.partner_relation: str = partner_relation #ally or enemy
        self.win_rate: float = win_rate
        self.pick_rate: float = pick_rate
        self.number_of_games: int = number_of_games

    def __str__(self):
        # Create a dictionary of all the instance attributes
        data = {
            "champion_name": self.champion_name,
            "champion_role": self.champion_role,
            "partner_champion_name": self.partner_champion_name,
            "partner_role": self.partner_role,
            "partner_relation": self.partner_relation,
            "win_rate": self.win_rate,
            "pick_rate": self.pick_rate,
            "number_of_games": self.number_of_games
        }
        # Convert dictionary to JSON string
        return json.dumps(data)
    
    def __repr__(self):
        return self.__str__()
