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
    {
        "balances": {
            "available": {
                "HIVE": 0.036,
                "HBD": 0.0,
                "VESTS": 76381.990195
            },
            "savings": {
                "HIVE": 0.0,
                "HBD": 0.0
            },
            "rewards": {
                "HIVE": 0.0,
                "HBD": 0.0,
                "VESTS": 0.0
            },
            "total": {
                "HIVE": 0.036,
                "HBD": 0.0,
                "VESTS": 76381.990195
            }
        },
        "voting_power": 99.43,
        "reputation": 51.92520108034113,
        "name": "slashformotion",
        "profile": {
            "profile_image": "https://cdn.pixabay.com/photo/2015/06/08/15/11/camera-801924_960_720.jpg",
            "cover_image": "https://dtxu61vdboi82.cloudfront.net/2018-01-01/ebb5aec4-a67c-4838-aba4-9aa7fd66ae02.jpeg",
            "name": "Slashformotion",
            "about": "Compte Principal : @theophile.roos ",
            "location": "France",
            "website": "https://alpha.steepshot.io/@slashformotion"
        },
        "vote_value": 0.00012391208202342324,
        "complete_recharge_vote_time_str": "0:41:00",
        "downvoting_power": 100.0,
        "curation_stats": {
            "24hr": 0.0,
            "7d": 0.005001926271379387,
            "avg": 0.000714560895911341
        },
        "creator": "steem",
        "__signature__": "JPdcMsgPCIeEazKv58pEsvuXUllExxuX2d4I60b60uhwHO7wb2nx4QO9Ug79CZkP5KepPf9ULQhTEQz2qmUuhQnPh35Pd2sFnSdcVFBP799OD6BuDxIjnDfm1GN57ut9nnFkcmlQyAD33BZLOSXrYV5XUxOXuNwsZ302OwGIXMtvLnDaytKpypv7bNf2DVuCbwnuI5BN1pRIpoPsXrutk8SsxNj3b4SpFAhNbIJt94rjHXRLAqI6Azv318JVS368QHOtOClmd3pfO8UnGU69QoqTFqg5VkM1D4XDAF9DgCfhhJLTBFGCPIv2FVKHttF8eLvZG4UCpQflHgIYJDmT85KNSZheE7ABOKbl6hrpqYwrqKIPTk7roQoNlgvC3BVxPDGDWArOfmL4xVMP",
        "__date__": "14:44 23,July,2020"
    }
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
                  "curation_stats": self.curation_stats,
                  "creator": self.creator,
                  "RC_pct": self.RC_pct
                  
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

    @property
    def curation_stats(self):
        stats = self.acc.curation_stats()
        return stats

    @property
    def creator(self):
        creator = self.acc.get_creator()
        if creator == None:
            return 'none'
        else:
            return creator
    
    @property
    def RC_pct(self):
        return self.RC.get('current_mana_pct')

    @property
    def RC(self):
        return self.acc.get_manabar()

    
    # def get_comment_history(self):
    #     return self.acc.

if __name__ == "__main__":
    from pprint import pprint
    
    e = HiveAccount("theophile.roos", hive_instance=hive_instance)

    

    print("Profile : ")
    pprint(e.curation_stats.get("avg"))
    print()
    pprint(type(e.curation_stats.get("avg")))

