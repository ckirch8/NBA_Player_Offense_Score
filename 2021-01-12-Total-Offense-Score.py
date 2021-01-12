#!/usr/bin/env python
# coding: utf-8

# # Total Offense Score
# 
# The goal of this article is to create a new metric to judge a single player's offensive production. I know there is a ton out there already (PER, OWS, OBPM, etc.) but I wanted to try my hand at creating one and possibly find ways improve upon them. My metric will mostly be based on total production and how efficient that player was at achieving that production.
# 
# ### Method
# 
# I measured total production as points generated ($PGEN$), which is the sum of the points the player generated either through scoring or passing, for which we will include second assists and free throw assists. The formula is as follows:
# 
# $$PGEN = PTS + \frac{AST\:PTS\:CREATED}{AST + FT\:AST} * (AST + 2nd\:AST + FT\:AST)$$
# 
# We are getting our stats from nba.com/stats, which includes $FT\:AST$ in their calculation for AST\:PTS\:CREATED but does not include 2nd\:AST so we find the player's points per assist and multiply that by the total of the three types to estimate the total points generated through passing.
# 
# To measure efficiency I will be using a stat called Individual Offensive Efficiency with Assist Opportunities ($IOEwAO$) which is $PGEN$ divided by the number or possessions that player terminated ($NPTwAO$) either by shooting, making a pass that leads to a shot, or turning the ball over. I know those are complicated abbreviations but $IOEwAO$ can differ from just Individual Offensive Efficiency which doesn't take into account potential assists. I will be using assist opportunities as it is more indicative of how often that player ends a possession.
# 
# $$NPTwAO = FGA + .44*FTA + TOV + ASSIST\:OPORTUNITIES + 2nd\:AST - OREB$$
# 
# $$IOEwAO = \frac{PGEN}{NPTwAO}$$
# 
# You may notice that I included offensive rebounds in the $NPTwAO$ calculation, this is because NPT stands for net possessions terminated and offensive rebound earns the team another possession. Also, $FT\:AST$ was not included because on on nba.com/stats $ASSIST\:OPORTUNITIES$ and $FT\:AST$ overlap.
# 
# We multiply free throws by 0.44 since not every time does a player shoot two free throws for a foul. 0.44 gives us a better estimate of the actual number of possessions.
# 
# Ok so this is the bulk of the information that will be used, now I have to get the data. Using the nba_api repository on github, I wrote a Python Script to scrape the necessary data for every active player in the 2019-20 NBA season into a spreadsheet, and calculated their $PGEN$, $NPTwAO$, and $IOEwAO$ along with some other metrics that this article will not focus on. 

# In[39]:


import pandas as pd

df = pd.read_csv('offensive_efficiency_19_20.csv')
df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'PTS', 'FGA', 'FTA', 
    'TOV', 'OREB', 'PGen', 'NPTwAO', 'PGen/G', 'NPTwAO/G', 'IOEwAO']].head(10)


# The full spreadsheet contains 41 columns. If you are interested in checking it out, it can be found here, but the above columns are what we are going to use in ths article.

# First let's find the league average in points per posession. This can be closely estimated by dividing the total points by the total possesions, using the .44 weight for free throws mentioned before. 
# 
# $$PPP = \frac{PTS}{FGA + .44*FTA + TOV - OREB}$$

# In[40]:


ppp = df['PTS'].sum() / (df['FGA'].sum() + .44*df['FTA'].sum() + df['TOV'].sum() - df['OREB'].sum())
print(ppp)


# So roughly 1.09 points are scored per possession in the NBA. Having an $IOEwAO$ above this would mean the player produces points at an above average rate, which is good, and should be rewarded in our metric. A below average rate should be punished. To accomplish this, I will take the players $PGEN/G$ and raise it to the power of their $IOEwAO$ divided by $PPP$ which we will call the efficiency factor.
# 
# $$PGEN/G^{\frac{IOEwAO}{PPP}}$$
# 
# This makes it so a player's $PGEN/G$ value increases at an exponential rate if it was done on good efficiency, and decreases at an exponential rate on poor efficiency.
# For example:

# In[29]:


print('PGen = 30, IOEwAO = 1, Score =', 30**(1/1.087))
print('PGen = 30, IOEwAO = 1.2, Score =', 30**(1.2/1.087))


# Using this, lets see how players stack up against each other. Note that this is a average per game metric which differs from some like OWS and OPBM.

# In[30]:


df['Score'] = df['PGen/G'] ** (df['IOEwAO'] / ppp)
df[['PLAYER_NAME', 'NPTwAO/G', 'PGen/G', 'IOEwAO', 'Score']].sort_values('Score', ascending = False).head(25)


# This is the top 25 players ranked by our new score.
# 
# Our current formula would tell us that last year, Mitchell Robinson was one of the most productive offensive players in the league. It's understandable if you don't believe this, but he did have a superb IOEwAO at 2.005, much better than the rest of the top 25. However, if you notice, he only had about 5.5 possessions terminated a game so it was much easier to reach his high efficiency compared to the number 1 player, Damian Lillard, who had 42 possessions terminated per game.
# 
# This is a flaw that we need to account for. To do this I will introduce another equation and variable called possession weight.
# 
# $$POS\:WT = 1 - 10^{-(\frac{NPTwAO/G}{Average\:NPTwAO/G})}$$
# 
# Now this is a little complicated so I will do my best to explain. Basically possession weight will come out with a value in between 0 and 1. The larger the player's $NPTwAO/G$, the closer to 1 and visa versa. The score from above will be multiplied by this weight. Below is a plot of the weights by $NPTwAO/G$.

# In[31]:


import matplotlib.pyplot as plt

npt_avg = df['NPTwAO'].sum() / df['GP'].sum()

fig, ax = plt.subplots(1, 1, figsize=(10, 4))
plt.plot(df['NPTwAO/G'], (1 - 10 ** (-1*df['NPTwAO/G'] / npt_avg)), '.', alpha=.5)
plt.axvline(14.3, color='k', linestyle='dashed', linewidth=1)
# print(df['NPTwAO/G'].mean())
plt.show()


# If the player's $NPTwAO/G$ is equal to the league average, the weight comes out to 0.90, which is the dotted vertical line. High above the average and the score will barely change as the weight get closer to 1, way below and it is affected significantly.
# 
# ### Results
# 
# Now let's look at our new updated rankings.

# In[42]:


df['Eff_Factor'] = (df['IOEwAO'] / ppp)
df['Pos_Weight'] =  (1 - 5 ** (-1*df['NPTwAO/G'] / npt_avg))
df['Score'] = df['PGen/G'] ** df['Eff_Factor'] * df['Pos_Weight']


df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'NPTwAO/G', 'PGen/G', 'IOEwAO', 'Eff_Factor', 'Pos_Weight', 'Score']].to_csv('player_score_results.csv')

df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'NPTwAO/G', 'PGen/G', 'IOEwAO', 'Eff_Factor', 'Pos_Weight', 'Score']].sort_values('Score', ascending = False).head(25)


# Based on our new offensive score metric, these were the top 25 offensive players of the 2019-20 season. Note that a few of these players, like Steph Curry and Kyrie Irving missed a lot of games but had hish scores the games they did play. Outside of that, I would say this is a pretty reasonable list, to make it to the top you need both volume and efficiency. I also believe playmaking is better rated in this metric than others by including assist opportunities, 2nd assists, and free throw assists.
# 
# What I like most about this metric is that volume at the cost of efficiency will hurt your score. For example, lets take an estimated Damian Lillard game where he has 42 NPTwAO and 52 PGen. Now let's say he continues to take 5 more shots, and makes 2 of them shooting 40% for 4 points, only producing .8 ppp. He would now have 47 NPTwAO and 56 PGen. Let's look at the difference in final scores between the two instances of the game.

# In[35]:


score = 52 ** ((52/42)/ppp) * (1 - 5 ** (-1*42 / npt_avg))
print('Score before shots', score)
score_final = 56 ** ((56/47)/ppp) * (1 - 5 ** (-1*47 / npt_avg))
print('Score after shots', score_final)


# One flaw I have with PER, whose formula can be found here, is that a player can improve their score with volume as long as they are shooting above 30.4% from the field. If I had a player shooting around 35%, I would not want him to increase his volume. My metric makes it so increasing volume is curved by the efficiency factor heavily so that volume is only good when they are producing above league average efficiency.

# ### Flaws
# 
# Now I will admit there are some flaws to this metric. Being a purely offensive stat focused metric, it leaves out stats like defensive rebounds, blocks, and steals which could lead to offensive possessions and may unfairly omit a good defender's actual contribution. It doesn't adjust for pace so plyers on teams that play faster might get more opportunities to generate points leading to higher scores. Using assist opportunities puts reliance on teammates to make shots, so a player's playmaking score might be a lot lower on a bad team than it would a good team, as you probably noticed there are only a few instances of a player on a bad team. I didn't really know how to go about this because leaving out unconverted opportunities misconstrues that player's usage, but if I were to try and regularize the conversion of assist opportunities it may unfairly punish those who set up their teammates better which is why their team is better in the first place.
# 
# This isn't really a flaw in the stat but another issue is that 2nd assists, free throw assists, and assist opportunities only go back to the 13-14 season when player tracking started so we will be unable to compare offensive scores historically unfortunately, unless we figure out a way to estimate these stats.

# ### Conclusion
# 
# I feel this is a good metric to compare offensive performances. This is not to show how skilled a player is necessarily as a lot of it is based on opportunity, but all the time we spend on comparing performance, I think this metric does a better job than most when it comes to offense. It can be used for single game matchups as well as whole seasons differentiating itself to metrics like offensive win shares, and in my opinion pretty unbiased to position.
# 
# While there are some flaws and can get a bit complicated, I believe this is a simpler metric to understand than other popular ones that get even more complicated, as it can be boiled down to pretty much volume affected by efficiency. A future task would be to figure out how to incorporate defense which can be extremely hard to measure in numbers.
