import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''All data comes from Lahman's Baseball Database available at http://www.seanlahman.com/baseball-archive/statistics/ 
This is some basic tinkering with just a massive database to practice skills with Pandas and seaborn libraries in Python.
'''

batting_csv = '/Users/franksyrek/Downloads/baseballdatabank-2019.2/core/Batting.csv'
people_csv = '/Users/franksyrek/Downloads/baseballdatabank-2019.2/core/People.csv'
teams_csv = '/Users/franksyrek/Downloads/baseballdatabank-2019.2/core/Teams.csv'
salaries_csv = '/Users/franksyrek/Downloads/baseballdatabank-2019.2/core/Salaries.csv'
batting_df = pd.read_csv(batting_csv)
people_df = pd.read_csv(people_csv)
teams_df = pd.read_csv(teams_csv)
salaries_df = pd.read_csv(salaries_csv)

batting_df.fillna({'lgID':'NA','G': 0, 'AB': 0, 'R': 0, 'H': 0, '2B': 0, '3B': 0, 'HR': 0, 'RBI': 0, 'SB': 0, 'CS': 0, 'BB': 0, 'SO': 0, 'IBB': 0, 'HBP': 0, 'SH': 0, 'SF': 0, 'GIDP': 0},inplace = True)
people_df.fillna({'weight': 0, 'height': 0}, inplace= True)
people_df.astype({'weight':int, 'height':int, 'bats': 'category', 'throws': 'category','debut':'datetime64'}, categories = ['left', 'right', 'both'])
batting_df.astype({'yearID':int,'G': int, 'AB': int, 'R': int, 'H': int, '2B': int, '3B': int, 'HR': int, 'RBI': int, 'SB': int, 'CS': int, 'BB': int, 'SO': int, 'IBB': int, 'HBP': int, 'SH': int, 'SF': int, 'GIDP': int})
batting_df.astype({'lgID':'category'}, categories =['NA', 'NL', 'AL'])
batting_df.astype({'teamID':'category'})
teams_df.fillna({'lgID': 'NA', 'Ghome':-1}, inplace = True)
teams_df.fillna({ 'R':-1, 'AB':-1,'H':-1, '2B':-1, '3B':-1, 'HR':-1, 'BB': -1, 'SO':-1, 'SB':-1, 'CS':-1, 'HBP':-1, 'SF':-1, 'RA': -1, 'ER': -1, 'ERA':-1, 'CG':-1, 'SHO':-1, 'SV':-1, 'IPouts': -1, 'HA':-1, 'HRA':-1, 'BBA': -1, 'SOA': -1, 'E':-1, 'DP':-1, 'FP':-1, 'attendance':-1, 'BPF':-1, 'PPF':-1}, inplace = True)
teams_df.astype({'yearID':int, 'lgID': 'category','Rank':int, 'G':int, 'W':int, 'L':int, 'Ghome':int}, categories =['NA', 'NL', 'AL'])
teams_df.astype({ 'R':int, 'AB':int,'H':int, '2B':int, '3B':int, 'HR':int, 'BB': int, 'SO':int, 'SB':int, 'CS':int, 'HBP':int, 'SF':int, 'RA': int, 'ER': int, 'ERA':int, 'CG':int, 'SHO':int, 'SV':int, 'IPouts': int, 'HA':int, 'HRA':int, 'BBA': int, 'SOA': int, 'E':int, 'DP':int, 'FP':int, 'attendance':int, 'BPF':int, 'PPF':int})
salaries_df.astype({'salary':int, 'lgID': 'category'}, categories = ['NL', 'AL'])


drop_0_AB = batting_df.loc[batting_df['AB'] > 0] #prevents future divide by zero errors

drop_0_weight =people_df.loc[people_df['weight'] != 0] #removes players withno listed height
drop_0_player = drop_0_weight.loc[drop_0_weight['height']!= 0] #removes players with no listed weight


drop_0_AB['avg'] = drop_0_AB['H']/drop_0_AB['AB'] #add batting avg to batting table
drop_0_AB['RBI_per_AB'] = drop_0_AB['RBI']/drop_0_AB['AB']

player_batting_df = drop_0_AB.merge(drop_0_player, how = 'left', on= 'playerID') #left merge allows players to map to more than one years batting data
batting_player_sal_df = player_batting_df.merge(salaries_df, how = 'inner', on = ['playerID', 'yearID', 'teamID', 'lgID'])





def standardize(x, mean, std):#calculates z score for each data point
	if(std == 0):
		std = 0.0001
	return (x-mean)/std 

def z_score(x):
	mean = x.mean()
	std = x.std(ddof=0)
	return x.apply(standardize, args = (mean, std))

def correlation(a,b): #uses Pearsons r and uncorrected std 
	a_mean = a.mean()
	a_std = a.std(ddof = 0)
	b_mean = b.mean()
	b_std = b.std(ddof=0)
	c = a.apply(standardize, args =(a_mean,a_std))
	d = b.apply(standardize, args = (b_mean, b_std))
	e = c*d
	return e.mean()

def to_bool(x):
	if x == "Y":
		return True
	return False

def bool_wrapper(df, col):
	return df[col].apply(to_bool)

def correlation_wrapper(x, y,z):
	return correlation(x[y], x[z]) 

def max_wrapper(x):
	return x['salary'].max()


arr = ['DivWin', 'WCWin', 'LgWin', 'WSWin']
for x in arr:  								#changes Y/N values into python bools
	teams_df[x] = bool_wrapper(teams_df,x)

prop = batting_player_sal_df.groupby(['yearID', 'teamID'])
team_sal_by_year = prop['salary'].apply(np.sum)

teams_df['salary'] = -1
standardized_df = pd.DataFrame()
standardized_df[['playerID', 'yearID']] = batting_player_sal_df[['playerID', 'yearID']]
arr = np.arange(1985,2017) #adds total team salary to team df
for x in arr:
	per_year = salaries_df.loc[salaries_df['yearID'] == x]
	team_sal = per_year.groupby('teamID')
	tea = team_sal['salary'].apply(np.sum)
	teams_df.loc[teams_df['yearID']== x, 'salary'] = tea.values
	mean = tea.mean()
	std = tea.std()
	ZSCORE = tea.apply(standardize,args =(mean,std))
	teams_df.loc[teams_df['yearID']==x, 'sal_score'] =ZSCORE.values
	yearly = batting_player_sal_df.loc[batting_player_sal_df['yearID'] == x]
	mean = yearly['H'].values.mean()
	std = yearly['H'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'H'] =yearly['H'].apply(standardize, args=(mean, std)).values
	mean = yearly['R'].values.mean()
	std = yearly['R'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'R'] =yearly['R'].apply(standardize, args=(mean, std)).values
	mean = yearly['2B'].values.mean()
	std = yearly['2B'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, '2B'] =yearly['2B'].apply(standardize, args=(mean, std)).values
	mean = yearly['3B'].values.mean()
	std = yearly['3B'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, '3B'] =yearly['3B'].apply(standardize, args=(mean, std)).values
	mean = yearly['HR'].values.mean()
	std = yearly['HR'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'HR'] =yearly['HR'].apply(standardize, args=(mean, std)).values
	mean = yearly['RBI'].values.mean()
	std = yearly['RBI'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'RBI'] =yearly['RBI'].apply(standardize, args=(mean, std)).values
	mean = yearly['SB'].values.mean()
	std = yearly['SB'].values.std()
	mean = yearly['SO'].values.mean()
	std = yearly['SO'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'SO'] =yearly['SO'].apply(standardize, args=(mean, std)).values
	standardized_df.loc[standardized_df['yearID']==x, 'SB'] =yearly['SB'].apply(standardize, args=(mean, std)).values
	mean = yearly['BB'].values.mean()
	std = yearly['BB'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'BB'] =yearly['BB'].apply(standardize, args=(mean, std)).values
	mean = yearly['IBB'].values.mean()
	std = yearly['IBB'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'IBB'] =yearly['IBB'].apply(standardize, args=(mean, std)).values
	mean = yearly['GIDP'].values.mean()
	std = yearly['GIDP'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'GIDP'] =yearly['GIDP'].apply(standardize, args=(mean, std)).values
	mean = yearly['height'].values.mean()
	std = yearly['height'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'height'] =yearly['height'].apply(standardize, args=(mean, std)).values
	mean = yearly['avg'].values.mean()
	std = yearly['avg'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'avg'] =yearly['avg'].apply(standardize, args=(mean, std)).values
	
	mean = yearly['AB'].values.mean()
	std = yearly['AB'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'AB'] =yearly['AB'].apply(standardize, args=(mean, std)).values
	mean = yearly['RBI_per_AB'].values.mean()
	std = yearly['RBI_per_AB'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'RBI_per_AB'] =yearly['RBI_per_AB'].apply(standardize, args=(mean, std)).values
	mean = yearly['salary'].values.mean()
	std = yearly['salary'].values.std()
	standardized_df.loc[standardized_df['yearID']==x, 'salary'] =yearly['salary'].apply(standardize, args=(mean, std)).values


sns.set()
sns.set_context("paper")



#Returns a Pandas Series with each years average hits and a graph
def hits_by_year_mean():
	batting_per_year = player_batting_df.groupby('yearID')
	hits_per_year = batting_per_year['H'].mean()
	hits_per_year.plot()
	plt.show()
	print(batting_per_year['H'].mean())

#Returns a Pandas Series with each years max hits and a graph
def hits_by_year_max():
	batting_per_year = player_batting_df.groupby('yearID')
	hits_per_year = batting_per_year['H'].max()
	hits_per_year.plot()
	plt.show()
	print(batting_per_year['H'].max())

def games_per_year_mean():
	batting_per_year = player_batting_df.groupby('yearID')
	hits_per_year = batting_per_year['G'].mean()
	hits_per_year.plot()
	plt.show()
	print(batting_per_year['G'].mean())

def games_per_year_max():
	batting_per_year = player_batting_df.groupby('yearID')
	hits_per_year = batting_per_year['G'].max()
	hits_per_year.plot()
	plt.show()
	print(batting_per_year['G'].max())

def homers_per_year_mean():
	batting_per_year = player_batting_df.groupby('yearID')
	hits_per_year = batting_per_year['HR'].mean()
	hits_per_year.plot()
	plt.show()
	print(batting_per_year['HR'].mean())

def homers_per_year_max():
	batting_per_year = player_batting_df.groupby('yearID')
	hits_per_year = batting_per_year['HR'].max()
	hits_per_year.plot()
	plt.show()
	print(batting_per_year['HR'].max())



#notice with this graph what years contain the outliers
def homers_vs_walks():
	sns.scatterplot(x = 'HR', y = 'BB', hue = 'yearID', data = player_batting_df, palette = 'coolwarm')
	plt.show()



def homers_vs_strikeouts():
	sns.scatterplot(x = 'HR', y = 'SO', hue = 'yearID', data = player_batting_df, palette = 'coolwarm')
	plt.show()
	
 




min_50_H = player_batting_df.loc[player_batting_df['H']>=50]

#using min 50 hits as a filter
def correlation_hits_homers_by_year():
	out = pd.Series(np.zeros(len(set(min_50_H['yearID']))), index = set(min_50_H['yearID']))
	for year in set(min_50_H['yearID']):
		out[year] = correlation_wrapper(min_50_H.loc[min_50_H['yearID'] == year], 'H', 'HR')
	out.plot()
	plt.show()
	print(out)

#only have salary data after 1985
def world_series_winner_salary_zscore():
	print(teams_df)
	has_salary_info = teams_df.loc[teams_df['yearID'] >= 1985]
	world_series_winner = has_salary_info.loc[has_salary_info['WSWin'] == True]
	print(world_series_winner)
	world_series_winner.plot(x = 'yearID', y = 'sal_score')
	plt.show()

















