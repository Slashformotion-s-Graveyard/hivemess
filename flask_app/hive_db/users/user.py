# account.py
from datetime import timedelta

from beem.account import Account
from beem.exceptions import AccountDoesNotExistsException

from .nodes import hive_instance

def account_exists(username):
    account = HiveAccount(username)
    exists = account.exists
    del account
    return exists


class HiveAccount(object):

    """
    {'balances': {'available': {'HBD': 0.071,
                            'HIVE': 0.029,
                            'VESTS': 216422.272937},
              'rewards': {'HBD': 0.0, 'HIVE': 0.0, 'VESTS': 0.0},
              'savings': {'HBD': 0.0, 'HIVE': 0.0},
              'total': {'HBD': 0.071, 'HIVE': 0.029, 'VESTS': 216422.272937}},
    'complete_recharge_vote_time_str': '1:19:33',
    'downvoting_power': 100.0,
    'name': 'theophile.roos',
    'profile': {'about': "Arpenteur d'internet, je partage ce qui me passe sous "
                        'le nez !',
                'cover_image': 'https://dtphgwb5vjcez.cloudfront.net/optim/focus/news/10/10164/RED_WEAPON8K_01.jpg',
                'location': 'France',
                'name': 'Théophile Roos',
                'profile_image': 'https://steemit-production-imageproxy-thumbnail.s3.amazonaws.com/DQmSd8u145jjJEoQRcWT1P2btDGq74X2kCiVUdE1MBzGupk_1680x8400',
                'website': 'https://d.tube/#!/c/theophile.roos'},
    'reputation': 53.403808184185685,
    'vote_value': 0.0005071412028735301,
    'voting_power': 98.89}
    """
    def __init__(self, name, hive_instance=hive_instance):
        try:
            self.acc = Account(name, steem_instance=hive_instance)
        except AccountDoesNotExistsException as e:
            print(e)
            self.__exists = False
        else:
            self.__exists = True

    def get_report(self):
        """
        return a full report on the account

        Returns:
            dict: report
        """
        report = {"balances": self.balances,
                  "voting_power": self.voting_power,
                  "reputation": self.reputation,
                  "name": self.name,
                  "profile": self.profile,
                  "vote_value": self.vote_value,
                  "voting_power": self.voting_power,
                  "complete_recharge_vote_time_str": self.complete_recharge_vote_time_str,
                  "downvoting_power": self.downvoting_power,
                  }
        return report

    @property
    def exists(self):
        return self.__exists

    @property
    def balances(self):
        """
        return the actual balances of the account

        Returns:
            dict: ex : {'available': {'HBD': 0.098, 'HIVE': 13.142, 'VESTS': 190377.916911}, 'rewards': {'HBD': 0.0, 'HIVE': 0.0, 'VESTS': 0.0}, 'savings': {'HBD': 0.0, 'HIVE': 0.0}, 'total': {'HBD': 0.098, 'HIVE': 13.142, 'VESTS': 190377.916911}}
        """
        if not self.exists:
            return None
        raw_balance = self.acc.balances
        balances = dict()
        for k, v in raw_balance.items():
            montants = dict()
            for montant in v:
                montants[montant.tuple()[1]] = montant.tuple()[0]
            balances[k] = montants
        return balances

    @property
    def voting_power(self):
        """
        return the voting power in percentage (0-100 range)

        Returns:
            int: voting power (0-100 range)
        """
        return round(self.acc.vp, ndigits=2)

    @property
    def downvoting_power(self):
        return round(self.acc.get_downvoting_power(), 2)

    @property
    def reputation(self):
        # in percentage
        return self.acc.rep

    @property
    def name(self):
        return self.acc.name

    @property
    def profile(self):
        """
        return the profile 

        Returns:
            dict: return profile with keys ['about','cover_image','location':,'name','profile_image','website']
        """
        return self.acc.profile

    @property
    def vote_value(self):
        """
        return voting value in HIVE

        Returns:
            float: voting value
        """
        return self.acc.get_voting_value()

    @property
    def complete_recharge_vote_time_str(self):
        """
        return str to complete recharge of vote capacity

        Returns:
            [type]: [description]
        """
        return self.acc.get_recharge_time_str(voting_power_goal=100)


if __name__ == "__main__":
    from pprint import pprint
    
    e = HiveAccount("theophile.roos", hive_instance=hive_instance)

    

    print("Profile : ")
    pprint(e.get_report())
    print()
