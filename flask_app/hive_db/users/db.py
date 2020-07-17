import pathlib as pl
import json
from .utils import get_now, get_now_minus_timedelta
from .user import HiveAccount, account_exists
import datetime 

class HiveUserDB(object):
    def __init__(self):
        self.__self_path = pl.Path(__file__).parent
        self.__userDB_path = self.__self_path / pl.Path("userDB/")
        self.date_filter = "%H:%M %d,%B,%Y"
        self.filter_days = {'days':1}


    def __get_usernames_stored(self):
        usernames = []
        for json_file_path in self.__get_json_paths():
            usernames.append(json_file_path.stem)
        return usernames

    def __get_json_paths(self):
        for json_file_path in self.__userDB_path.rglob('*.json'):
            yield json_file_path
        
    
    def __get_data(self, username):
        # we assume that the user is in the userDB
        user_data = None
        path_to_user_json = self.__userDB_path / pl.Path("{username}.json".format(username=username))
        with path_to_user_json.open('r') as f:
                user_data = json.load(f)
        return user_data

    def get_user(self, username):
        if username in self.__get_usernames_stored():

            data_not_checked = self.__get_data(username)
            try :
                data_checked = self.__unsign(data_not_checked)
            except RuntimeError as e:
                print(f"[ERROR]in db.py : {e}")
                if account_exists(username):
                    user_data = HiveAccount(username).get_report()
                    data_signed = self.__sign(user_data)
                    self.__dump(username, data_signed)
                    return user_data
                else:
                    return None
            else:
                return data_checked
        else:
            if account_exists(username):
                user_data = HiveAccount(username).get_report()
                data_signed = self.__sign(user_data)
                self.__dump(username, data_signed)
                return user_data
            else:
                return None

    def __dump(self, username, data_user):
        if not (type(username) is str and type(data_user) is dict):
            raise TypeError("Wrong argument typing, it should be <str,dict>")
        path_to_user_json = self.__userDB_path / pl.Path("{username}.json".format(username=username))
        with path_to_user_json.open('w') as f:
                json.dump(data_user, f, indent=4)

    def __sign(self, user_data):
        user_data = dict(user_data)
        user_data["__signature__"] = self.signature
        user_data['__date__'] =  get_now().strftime(self.date_filter)
        return user_data        
       
    def __unsign(self, user_data):
        user_data = dict(user_data)
        
        if user_data.get("__signature__", 'novalue') != self.signature or '__date__' not in user_data:
            raise RuntimeError(f"Data retreived for user <{user}> was not signed ")

        # retreive original datetime object
        user_data['__date__'] = datetime.datetime.strptime(user_data['__date__'],self.date_filter)
        if user_data.get("__date__") < get_now_minus_timedelta(**self.filter_days):
            raise RuntimeError(f"Data too old")
        user_data.pop('__signature__')
        return user_data


    
    @property
    def signature(self):
        return 'JPdcMsgPCIeEazKv58pEsvuXUllExxuX2d4I60b60uhwHO7wb2nx4QO9Ug79CZkP5KepPf9ULQhTEQz2qmUuhQnPh35Pd2sFnSdcVFBP799OD6BuDxIjnDfm1GN57ut9nnFkcmlQyAD33BZLOSXrYV5XUxOXuNwsZ302OwGIXMtvLnDaytKpypv7bNf2DVuCbwnuI5BN1pRIpoPsXrutk8SsxNj3b4SpFAhNbIJt94rjHXRLAqI6Azv318JVS368QHOtOClmd3pfO8UnGU69QoqTFqg5VkM1D4XDAF9DgCfhhJLTBFGCPIv2FVKHttF8eLvZG4UCpQflHgIYJDmT85KNSZheE7ABOKbl6hrpqYwrqKIPTk7roQoNlgvC3BVxPDGDWArOfmL4xVMP'



        
if __name__ == "__main__":
    h = HiveUserDB()
    print(h.get_usernames_stored())
    