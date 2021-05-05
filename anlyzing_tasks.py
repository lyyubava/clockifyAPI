from processing_requests import GetJsonData, GetInfo
import pandas as pd
import configuration

"""Розширити функціонал програми, щоб вона формувала на stdout загальний звіт (в т.ч. час потрачений на кожну задачу) 
по задачах, і по загальному часу потраченому на кожну з задач по груповані по датах. """


class Analyzes(GetInfo):

    def generate_df_for_task(self):
        """ returns pandas DataFrame for tasks total time spent for task group by task """
        df = {'Tasks': [task['description'] for task in self.get_time_entries()],
              'Duration': [task['timeInterval']['duration'] for task in self.get_time_entries()]}

        return df


if __name__ == '__main__':
    api_key = configuration.Configuration.X_API_KEY
    u = Analyzes(api_key)
    print(u.generate_df_for_task())
    df = u.generate_df_for_task()
    s = pd.DataFrame(df).groupby
    print(s)
