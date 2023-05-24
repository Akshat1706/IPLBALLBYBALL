import numpy as np
import pandas as pd

ball = pd.read_csv('F:\python\ipl\data.csv')
Matches = pd.read_csv('F:\python\ipl\Matches.csv')


ball = ball.merge(Matches, on='ID')
ball['BowlingTeam'] = np.where(ball['BattingTeam']==ball['Team1'],
                                       ball['Team2'],
                                       ball['Team1'])

Batsmen = ball.groupby('batter')\
            .agg({'ID':'nunique','batsman_run':'sum','isWicketDelivery':'sum'})\
            .reset_index()

Batsmen.columns = ['Batter','Innings','Runs','Dismissals']

BallsTaken = ball[(ball['extra_type']!='wides')].groupby('batter')['ID'].count().reset_index()
BallsTaken.columns = ['Batter','Balls Faced']

No4s = ball[(ball['batsman_run']==4)&(ball['non_boundary']==0)]\
            .groupby('batter')['ID']\
            .count()\
            .reset_index()\
            .sort_values('ID')
No4s.columns = ['Batter','4s']

No6s = ball[(ball['batsman_run']==6)&(ball['non_boundary']==0)]\
            .groupby('batter')['ID']\
            .count()\
            .reset_index()\
            .sort_values('ID')
No6s.columns = ['Batter','6s']

runs = ball.groupby(['batter','ID'])['batsman_run'].sum().reset_index()


HighScore = runs.groupby(['batter'])['batsman_run'].max().reset_index()
HighScore.columns = ['Batter','High Score']

No50s = runs[(runs['batsman_run']>=50)&(runs['batsman_run']<100)]\
        .groupby('batter')['batsman_run']\
        .count()\
        .reset_index()\
        .sort_values('batsman_run',ascending=False)
No50s.columns = ['Batter','50']

No100s = runs[(runs['batsman_run']>=100)]\
        .groupby('batter')['batsman_run']\
        .count()\
        .reset_index()\
        .sort_values('batsman_run',ascending=False)
No100s.columns = ['Batter','100']

Batsmen = Batsmen.merge(BallsTaken, on='Batter',how='outer').merge(No4s, on='Batter',how='outer')\
                     .merge(No6s, on='Batter',how='outer').merge(HighScore, on='Batter',how='outer')\
                     .merge(No50s, on='Batter',how='outer').merge(No100s, on='Batter',how='outer')

Batsmen['Strike Rate'] = (Batsmen['Runs']/Batsmen['Balls Faced'])*100
Batsmen['Batting Average'] = Batsmen['Runs']/Batsmen['Dismissals']

Batsmen.fillna(0, inplace=True)

Batsmen.sort_values(by='Runs', ascending=False)















