import re
import pandas as pd
import os

os.chdir('C:\Users\sojeo\SJ_practice\crawl_test_1\crawl_test_1')
df = pd.read_csv('cc_region.csv')

id_lst = list(set(df['insta_id']))
len(id_lst)

def del_foreign(df):
    id_lst = list(set(df['insta_id']))
    for user_id in id_lst:
        count = 0
        for y in list(df[df['insta_id']==user_id]['content']):
            if type(y) != str:
                pass
            elif re.search('[가-힣]', y):
                count += 1
        if count == 0:
            idx = df[df['insta_id']==user_id].index
            df.drop(idx, inplace=True)
    return df

new_df = del_foreign(df)

id_lst = list(set(new_df['insta_id']))
len(id_lst)