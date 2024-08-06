import json
import os
import time

from enum import Enum

from ..helpers import get_project_root


class UserDataKeys(Enum):
    THUMBNAIL_LINK = "THUMBNAIL_LINK"
    TIME_LAST_ACCESSED = "TIME_LAST_ACCESSED"


class UserData:

    DataFilePath = os.path.join(get_project_root(), "user_data")
    DataFileName = "{0}.json"

    def __init__(self, user_id: int):
        user_id = int(user_id)
        self.UserId = int(user_id)
        self.UserData = dict()
        self.UserDataFile = os.path.join(UserData.DataFilePath, UserData.DataFileName.format(user_id))
        self.__load_data()

    def __load_data(self):
        if not os.path.exists(UserData.DataFilePath):
            os.mkdir(UserData.DataFilePath)
        if not os.path.exists(self.UserDataFile):
            self.__save_data()
        with open(self.UserDataFile, 'r') as f:
            self.UserData = json.load(f)
        self.__initialize_user()

    def __save_data(self):
        with open(self.UserDataFile, 'w') as f:
            json.dump(self.UserData, f)

    def __initialize_user(self):
        for key in [data_key.value for data_key in UserDataKeys]:
            if key not in self.UserData.keys():
                self.UserData[key] = None

        self.__update_last_access()

    def __update_last_access(self):
        self.UserData[UserDataKeys.TIME_LAST_ACCESSED.value] = int(time.time())

    def get_data_value(self, data_key: UserDataKeys = None):
        self.__initialize_user()
        return self.UserData[data_key.value] if data_key else self.UserData

    def set_user_data(self, data_key: UserDataKeys, value):
        self.__initialize_user()
        self.UserData[data_key.value] = value
        self.__save_data()

    def set_character_sheet(self, sheet_details):
        for k, v in sheet_details.items():
            self.UserData[k] = v
        self.__save_data()
