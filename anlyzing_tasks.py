from processing_requests import GetJsonData, GetInfo
import pandas as pd
import configuration
import re
from typing import List
import datetime
import time


class Analyzes(GetInfo):

    @staticmethod
    def convert_duration(time: str) -> List:
        """converts time iso8601 format eg PT12S, PT20M26S, PT15S into a list:
        for example, for PT12S the output will be ['12S'], and for PT20M26S the output is ['20M', '26S']
        """
        result = re.findall('(\d+\D)', time)
        return result

    def convert(self, iso_dur: str) -> time:
        """ converts time iso8601 into a time like hh:mm:ss  for example for PT20M26S the output is 00:20:26
        """
        converted_dur = self.convert_duration(iso_dur)  # convert duration into a list
        n = len(converted_dur)
        converted_dur = [el[:-1] for el in converted_dur]
        converted_dur = ['0' + el if len(el) < 2 else el for el in converted_dur]
        while n < 3:
            converted_dur.insert(0, '00')
            n += 1
        return datetime.datetime.strptime(':'.join(converted_dur), '%H:%M:%S')
        # return ':'.join(converted_dur)

    def generate_df_for_task(self) -> dict:
        """ this is an auxiliary function that takes part in creating pandas DataFrame
            key: Task
            val:duration
        """
        df = {'Tasks': [task['description'] for task in self.get_time_entries()],
              'Duration': [self.convert(task['timeInterval']['duration']) for task in self.get_time_entries()]}

        return df

    @staticmethod
    def summa(t1, t2):
        """ calculates sum of time intervals """
        time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
        a = (t1 - time_zero + t2)
        return a

    def grouped_by_time(self) -> dict:
        """ returns dictionary of tasks and its total duration key: task's name, value: total amount of time spent on
        this task """
        d = {}
        keys_list = self.generate_df_for_task()['Tasks']
        values_list = self.generate_df_for_task()['Duration']
        for i in range(len(keys_list)):
            if keys_list[i] in d:
                d[keys_list[i]] = self.summa(d[keys_list[i]], values_list[i])
            else:
                d[keys_list[i]] = values_list[i]
        for key in d:
            d[key] = d[key].strftime('%H:%M:%S')
        return d

    def show_df_grouped_by_total_time(self):
        """prints pretty dstaframe for tasks grouped by total amount of time spent on it"""
        df = self.grouped_by_time()
        df = {'Task': [i for i in df.keys()], 'Duration': [j for j in df.values()]}
        df = pd.DataFrame(df)
        return df


if __name__ == '__main__':
    api_key = configuration.Configuration.X_API_KEY
    u = Analyzes(api_key)
    print(u.show())
    # print(u.generate_df_for_task())
    # arr = ['3H', '2M', '2S']
    # print(u.grouped_by())
    print(u.show1())
    # t1 = datetime.datetime(2,59,  59, '%H:%M:%S')
    # print(t1)
    # t1 = datetime.datetime.strptime(, '%H:%M:%S')
    # t2 = datetime.datetime.strptime('02:59:59', '%H:%M:%S')
    # print(t2.time())
    # time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    # print((t1 - time_zero + t2).time())
    # t1 = datetime.datetime.strptime('08:09:59', '%H:%M:%S')
    # t2 = datetime.datetime.strptime('02:59:59', '%H:%M:%S')
    # time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    # print((t1 - time_zero + t2))
