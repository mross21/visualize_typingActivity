"""
@author: Mindy Ross
python version 3.7.4
"""
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import glob

# sort files numerically
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return(parts)

pathKP = '/home/mindy/Desktop/BiAffect-iOS/UnMASCK/BiAffect_data/processed_output/keypress/'
pathOut = '/home/mindy/Desktop/BiAffect-iOS/UnMASCK/temporal_analyses/dotPlots_v2/'
all_files = sorted(glob.glob(pathKP + "*.parquet"), key = numericalSort)

for file in all_files:
    df = pd.read_parquet(file, engine='pyarrow')
    user = df['userID'].unique()[0]
    print(user)
    
    # select user
    u = 0
    if user != u:
        continue

    diag = '' # insert diagnosis for user here

    df['hour'] = pd.to_datetime(df['keypressTimestampLocal']).dt.hour
    df['kpCountPerHour'] = df.groupby(['hour','dayNumber'])['IKD'].transform('count')
    df['horiz_flag'] = np.where(df['upright'] == 'laying_down',1,0)
    df['percHoriz'] = df.groupby(['hour','dayNumber'])['horiz_flag'].transform('mean')

    plt.figure(figsize = (20,20))
    plt.style.use('ggplot')
    ax = plt.axes()
    ax.set_facecolor("whitesmoke")

    plt.scatter(df['hour'], df['date'], alpha = 1, s=df['kpCountPerHour'], c=df['percHoriz'])
    cbar = plt.colorbar(orientation='vertical')
    cbar.set_label(label='Fraction Laying Down',size=30, rotation=270,labelpad=40)
    cbar.ax.tick_params(labelsize=20)
    plt.xlabel('Hour',size=30)
    plt.title('User {} ({})'.format(user, diag),size=30)
    plt.ylabel('Date', size=30)
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    # plt.savefig(pathOut+'user_{}.png'.format(user))
    plt.show()
    # plt.close()
    break
    
print('finish')