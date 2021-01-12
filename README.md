
# Total Offense Score

The goal of this article is to create a new metric to judge a single player's offensive production. I know there is a ton out there already ([PER], [OWS], [OBPM], etc.) but I wanted to try my hand at creating one and possibly find ways improve upon them. My metric will mostly be based on total production and how efficient that player was at achieving that production.

### Method

I measured total production as points generated (PGEN), which is the sum of the points the player generated either through scoring or passing, for which we will include second assists and free throw assists. The formula is as follows:

$$PGEN = PTS + \frac{AST\:PTS\:CREATED}{AST + FT\:AST} * (AST + 2nd\:AST + FT\:AST)$$

We are getting our stats from [nba.com/stats], which includes FT AST in their calculation for AST PTS CREATED but does not include 2nd AST so we find the player's points per assist and multiply that by the total of the three types to estimate the total points generated through passing.

To measure efficiency I will be using a stat called Individual Offensive Efficiency with Assist Opportunities (IOEwAO) which is PGEN divided by the number or possessions that player terminated (NPTwAO) either by shooting, making a pass that leads to a shot, or turning the ball over. I know those are complicated abbreviations but IOEwAO can differ from just Individual Offensive Efficiency which doesn't take into account potential assists. I will be using assist opportunities as it is more indicative of how often that player ends a possession.

$$NPTwAO = FGA + .44*FTA + TOV + ASSIST\:OPPORTUNITIES + 2nd\:AST - OREB$$

$$IOEwAO = \frac{PGEN}{NPTwAO}$$

You may notice that I included offensive rebounds in the NPTwAO calculation, this is because NPT stands for net possessions terminated and offensive rebound earns the team another possession. Also, FT AST was not included because on nba.com/stats Assist Opportunities and FT AST overlap.

We multiply free throws by 0.44 since not every time does a player shoot two free throws for a foul. 0.44 gives us a better estimate of the actual number of possessions.

Ok so this is the bulk of the information that will be used, now I have to get the data. Using the [nba_api] repository on github, I wrote a [Python Script] to scrape the necessary data for every active player in the 2019-20 NBA season into a spreadsheet, and calculated their PGEN, NPTwAO, and IOEwAO along with some other metrics that this article will not focus on.


```python
import pandas as pd

df = pd.read_csv('offensive_efficiency_19_20.csv')
df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'PTS', 'FGA', 'FTA',
    'TOV', 'OREB', 'PGen', 'NPTwAO', 'PGen/G', 'NPTwAO/G', 'IOEwAO']].head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PLAYER_NAME</th>
      <th>TEAM_ABBREVIATION</th>
      <th>GP</th>
      <th>PTS</th>
      <th>FGA</th>
      <th>FTA</th>
      <th>TOV</th>
      <th>OREB</th>
      <th>PGen</th>
      <th>NPTwAO</th>
      <th>PGen/G</th>
      <th>NPTwAO/G</th>
      <th>IOEwAO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aaron Gordon</td>
      <td>ORL</td>
      <td>62</td>
      <td>894</td>
      <td>767</td>
      <td>224</td>
      <td>100</td>
      <td>107</td>
      <td>1501.200000</td>
      <td>1296.56</td>
      <td>24.212903</td>
      <td>21.27</td>
      <td>1.157833</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aaron Holiday</td>
      <td>IND</td>
      <td>66</td>
      <td>627</td>
      <td>563</td>
      <td>87</td>
      <td>88</td>
      <td>22</td>
      <td>1287.780876</td>
      <td>1133.28</td>
      <td>19.511831</td>
      <td>17.56</td>
      <td>1.136331</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Abdel Nader</td>
      <td>OKC</td>
      <td>55</td>
      <td>345</td>
      <td>263</td>
      <td>66</td>
      <td>43</td>
      <td>14</td>
      <td>449.268293</td>
      <td>391.04</td>
      <td>8.168514</td>
      <td>7.16</td>
      <td>1.148906</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Adam Mokoka</td>
      <td>CHI</td>
      <td>11</td>
      <td>32</td>
      <td>28</td>
      <td>4</td>
      <td>2</td>
      <td>7</td>
      <td>44.500000</td>
      <td>33.76</td>
      <td>4.045455</td>
      <td>3.07</td>
      <td>1.318128</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Admiral Schofield</td>
      <td>WAS</td>
      <td>33</td>
      <td>99</td>
      <td>92</td>
      <td>15</td>
      <td>7</td>
      <td>7</td>
      <td>143.705882</td>
      <td>128.60</td>
      <td>4.354724</td>
      <td>3.96</td>
      <td>1.117464</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Al Horford</td>
      <td>PHI</td>
      <td>67</td>
      <td>798</td>
      <td>709</td>
      <td>80</td>
      <td>80</td>
      <td>103</td>
      <td>1512.297945</td>
      <td>1156.20</td>
      <td>22.571611</td>
      <td>17.59</td>
      <td>1.307990</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Al-Farouq Aminu</td>
      <td>ORL</td>
      <td>18</td>
      <td>78</td>
      <td>86</td>
      <td>29</td>
      <td>17</td>
      <td>24</td>
      <td>137.400000</td>
      <td>140.76</td>
      <td>7.633333</td>
      <td>8.04</td>
      <td>0.976130</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Alec Burks</td>
      <td>PHI</td>
      <td>66</td>
      <td>993</td>
      <td>768</td>
      <td>265</td>
      <td>91</td>
      <td>48</td>
      <td>1522.879808</td>
      <td>1302.60</td>
      <td>23.073936</td>
      <td>20.02</td>
      <td>1.169108</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Alen Smailagic</td>
      <td>GSW</td>
      <td>14</td>
      <td>59</td>
      <td>40</td>
      <td>19</td>
      <td>11</td>
      <td>10</td>
      <td>93.000000</td>
      <td>66.36</td>
      <td>6.642857</td>
      <td>4.74</td>
      <td>1.401447</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Alex Caruso</td>
      <td>LAL</td>
      <td>64</td>
      <td>349</td>
      <td>291</td>
      <td>94</td>
      <td>53</td>
      <td>17</td>
      <td>679.244604</td>
      <td>603.36</td>
      <td>10.613197</td>
      <td>9.66</td>
      <td>1.125770</td>
    </tr>
  </tbody>
</table>
</div>



The full spreadsheet contains 41 columns. If you are interested in checking it out, it can be found on  my [github], but the above columns are what we are going to use in this article.

First let's find the league average in points per possession. This can be closely estimated by dividing the total points by the total possessions, using the .44 weight for free throws mentioned before.

$$PPP = \frac{PTS}{FGA + .44*FTA + TOV - OREB}$$


```python
ppp = df['PTS'].sum() / (df['FGA'].sum() + .44*df['FTA'].sum() + df['TOV'].sum() - df['OREB'].sum())
print(ppp)
```

    1.0873277667011825


So roughly 1.09 points are scored per possession in the NBA. Having an IOEwAO above this would mean the player produces points at an above average rate, which is good, and should be rewarded in our metric. A below average rate should be punished. To accomplish this, I will take the players PGEN/G and raise it to the power of their IOEwAO divided by PPP which we will call the efficiency factor.

$$PGEN/G^{\frac{IOEwAO}{PPP}}$$

This makes it so a player's PGEN/G value increases at an exponential rate if it was done on good efficiency, and decreases at an exponential rate on poor efficiency.
For example:


```python
print('PGen = 30, IOEwAO = 1, Score =', 30**(1/1.087))
print('PGen = 30, IOEwAO = 1.2, Score =', 30**(1.2/1.087))
```

    PGen = 30, IOEwAO = 1, Score = 22.85057844894064
    PGen = 30, IOEwAO = 1.2, Score = 42.724465491574115


Using this, lets see how players stack up against each other. Note that this is a average per game metric which differs from some like OWS and OPBM.


```python
df['Score'] = df['PGen/G'] ** (df['IOEwAO'] / ppp)
df[['PLAYER_NAME', 'NPTwAO/G', 'PGen/G', 'IOEwAO', 'Score']].sort_values('Score', ascending = False).head(25)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PLAYER_NAME</th>
      <th>NPTwAO/G</th>
      <th>PGen/G</th>
      <th>IOEwAO</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>90</th>
      <td>Damian Lillard</td>
      <td>42.07</td>
      <td>52.270929</td>
      <td>1.261881</td>
      <td>98.650533</td>
    </tr>
    <tr>
      <th>364</th>
      <td>Mitchell Robinson</td>
      <td>5.51</td>
      <td>11.190416</td>
      <td>2.049158</td>
      <td>94.762398</td>
    </tr>
    <tr>
      <th>215</th>
      <td>James Harden</td>
      <td>47.50</td>
      <td>56.209223</td>
      <td>1.200825</td>
      <td>85.596552</td>
    </tr>
    <tr>
      <th>383</th>
      <td>Nikola Jokic</td>
      <td>29.51</td>
      <td>38.220744</td>
      <td>1.324564</td>
      <td>84.630986</td>
    </tr>
    <tr>
      <th>424</th>
      <td>Rudy Gobert</td>
      <td>12.11</td>
      <td>19.491754</td>
      <td>1.621689</td>
      <td>83.896069</td>
    </tr>
    <tr>
      <th>312</th>
      <td>Kyrie Irving</td>
      <td>37.89</td>
      <td>46.461379</td>
      <td>1.254221</td>
      <td>83.747851</td>
    </tr>
    <tr>
      <th>221</th>
      <td>Jarrett Allen</td>
      <td>9.21</td>
      <td>15.802198</td>
      <td>1.734327</td>
      <td>81.657820</td>
    </tr>
    <tr>
      <th>325</th>
      <td>Luka Doncic</td>
      <td>45.48</td>
      <td>53.628274</td>
      <td>1.196849</td>
      <td>80.091785</td>
    </tr>
    <tr>
      <th>281</th>
      <td>Karl-Anthony Towns</td>
      <td>29.36</td>
      <td>37.659113</td>
      <td>1.309635</td>
      <td>79.078980</td>
    </tr>
    <tr>
      <th>319</th>
      <td>LeBron James</td>
      <td>44.95</td>
      <td>52.825918</td>
      <td>1.196271</td>
      <td>78.607847</td>
    </tr>
    <tr>
      <th>175</th>
      <td>Giannis Antetokounmpo</td>
      <td>37.82</td>
      <td>45.957049</td>
      <td>1.225386</td>
      <td>74.717450</td>
    </tr>
    <tr>
      <th>76</th>
      <td>Clint Capela</td>
      <td>11.53</td>
      <td>18.265734</td>
      <td>1.608916</td>
      <td>73.593774</td>
    </tr>
    <tr>
      <th>245</th>
      <td>John Collins</td>
      <td>18.46</td>
      <td>26.192835</td>
      <td>1.426170</td>
      <td>72.465101</td>
    </tr>
    <tr>
      <th>474</th>
      <td>Trae Young</td>
      <td>48.45</td>
      <td>55.033549</td>
      <td>1.158617</td>
      <td>71.573127</td>
    </tr>
    <tr>
      <th>133</th>
      <td>Domantas Sabonis</td>
      <td>24.42</td>
      <td>31.984065</td>
      <td>1.329774</td>
      <td>69.262019</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Ben Simmons</td>
      <td>32.90</td>
      <td>39.960157</td>
      <td>1.235801</td>
      <td>66.119093</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Anthony Davis</td>
      <td>28.05</td>
      <td>35.397849</td>
      <td>1.273747</td>
      <td>65.244666</td>
    </tr>
    <tr>
      <th>186</th>
      <td>Hassan Whiteside</td>
      <td>12.41</td>
      <td>18.975417</td>
      <td>1.542605</td>
      <td>65.070609</td>
    </tr>
    <tr>
      <th>42</th>
      <td>Bradley Beal</td>
      <td>41.69</td>
      <td>47.880432</td>
      <td>1.169778</td>
      <td>64.203828</td>
    </tr>
    <tr>
      <th>239</th>
      <td>Jimmy Butler</td>
      <td>30.16</td>
      <td>36.820908</td>
      <td>1.253294</td>
      <td>63.846615</td>
    </tr>
    <tr>
      <th>110</th>
      <td>DeMar DeRozan</td>
      <td>31.95</td>
      <td>38.943015</td>
      <td>1.230290</td>
      <td>63.028871</td>
    </tr>
    <tr>
      <th>444</th>
      <td>Stephen Curry</td>
      <td>35.49</td>
      <td>41.270000</td>
      <td>1.210690</td>
      <td>62.941262</td>
    </tr>
    <tr>
      <th>125</th>
      <td>Devin Booker</td>
      <td>39.49</td>
      <td>45.710849</td>
      <td>1.177698</td>
      <td>62.804072</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Bam Adebayo</td>
      <td>23.29</td>
      <td>30.257050</td>
      <td>1.319444</td>
      <td>62.653395</td>
    </tr>
    <tr>
      <th>282</th>
      <td>Kawhi Leonard</td>
      <td>35.24</td>
      <td>41.560621</td>
      <td>1.199544</td>
      <td>61.057069</td>
    </tr>
  </tbody>
</table>
</div>



This is the top 25 players ranked by our new score.

Our current formula would tell us that last year, Mitchell Robinson was one of the most productive offensive players in the league. It's understandable if you don't believe this, but he did have a superb IOEwAO at 2.005, much better than the rest of the top 25. However, if you notice, he only had about 5.5 possessions terminated a game so it was much easier to reach his high efficiency compared to the number 1 player, Damian Lillard, who had 42 possessions terminated per game.

This is a flaw that we need to account for. To do this I will introduce another equation and variable called possession weight.

$$POS\:WT = 1 - 10^{-(\frac{NPTwAO/G}{Average\:NPTwAO/G})}$$

Now this is a little complicated so I will do my best to explain. Basically possession weight will come out with a value in between 0 and 1. The larger the player's NPTwAO/G, the closer to 1 and visa versa. The score from above will be multiplied by this weight. Below is a plot of the weights by NPTwAO/G.


```python
import matplotlib.pyplot as plt

npt_avg = df['NPTwAO'].sum() / df['GP'].sum()

fig, ax = plt.subplots(1, 1, figsize=(10, 4))
plt.plot(df['NPTwAO/G'], (1 - 10 ** (-1*df['NPTwAO/G'] / npt_avg)), '.', alpha=.5)
plt.axvline(14.3, color='k', linestyle='dashed', linewidth=1)
# print(df['NPTwAO/G'].mean())
plt.show()
```


![](output_10_0.png)


If the player's NPTwAO/G is equal to the league average, the weight comes out to 0.90, which is the dotted vertical line. High above the average and the score will barely change as the weight get closer to 1, way below and it is affected significantly.

### Results

Now let's look at our new updated rankings.


```python
df['Eff_Factor'] = (df['IOEwAO'] / ppp)
df['Pos_Weight'] =  (1 - 5 ** (-1*df['NPTwAO/G'] / npt_avg))
df['Score'] = df['PGen/G'] ** df['Eff_Factor'] * df['Pos_Weight']


df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'NPTwAO/G', 'PGen/G', 'IOEwAO', 'Eff_Factor', 'Pos_Weight', 'Score']].to_csv('player_score_results.csv')

df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'NPTwAO/G', 'PGen/G', 'IOEwAO', 'Eff_Factor', 'Pos_Weight', 'Score']].sort_values('Score', ascending = False).head(25)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PLAYER_NAME</th>
      <th>TEAM_ABBREVIATION</th>
      <th>NPTwAO/G</th>
      <th>PGen/G</th>
      <th>IOEwAO</th>
      <th>Eff_Factor</th>
      <th>Pos_Weight</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>90</th>
      <td>Damian Lillard</td>
      <td>POR</td>
      <td>42.07</td>
      <td>52.270929</td>
      <td>1.261881</td>
      <td>1.160534</td>
      <td>0.991203</td>
      <td>97.782672</td>
    </tr>
    <tr>
      <th>215</th>
      <td>James Harden</td>
      <td>HOU</td>
      <td>47.50</td>
      <td>56.209223</td>
      <td>1.200825</td>
      <td>1.104382</td>
      <td>0.995224</td>
      <td>85.187778</td>
    </tr>
    <tr>
      <th>312</th>
      <td>Kyrie Irving</td>
      <td>BKN</td>
      <td>37.89</td>
      <td>46.461379</td>
      <td>1.254221</td>
      <td>1.153490</td>
      <td>0.985920</td>
      <td>82.568697</td>
    </tr>
    <tr>
      <th>383</th>
      <td>Nikola Jokic</td>
      <td>DEN</td>
      <td>29.51</td>
      <td>38.220744</td>
      <td>1.324564</td>
      <td>1.218183</td>
      <td>0.963854</td>
      <td>81.571881</td>
    </tr>
    <tr>
      <th>325</th>
      <td>Luka Doncic</td>
      <td>DAL</td>
      <td>45.48</td>
      <td>53.628274</td>
      <td>1.196849</td>
      <td>1.100726</td>
      <td>0.994006</td>
      <td>79.611701</td>
    </tr>
    <tr>
      <th>319</th>
      <td>LeBron James</td>
      <td>LAL</td>
      <td>44.95</td>
      <td>52.825918</td>
      <td>1.196271</td>
      <td>1.100194</td>
      <td>0.993638</td>
      <td>78.107706</td>
    </tr>
    <tr>
      <th>281</th>
      <td>Karl-Anthony Towns</td>
      <td>MIN</td>
      <td>29.36</td>
      <td>37.659113</td>
      <td>1.309635</td>
      <td>1.204453</td>
      <td>0.963238</td>
      <td>76.171910</td>
    </tr>
    <tr>
      <th>175</th>
      <td>Giannis Antetokounmpo</td>
      <td>MIL</td>
      <td>37.82</td>
      <td>45.957049</td>
      <td>1.225386</td>
      <td>1.126971</td>
      <td>0.985809</td>
      <td>73.657125</td>
    </tr>
    <tr>
      <th>474</th>
      <td>Trae Young</td>
      <td>ATL</td>
      <td>48.45</td>
      <td>55.033549</td>
      <td>1.158617</td>
      <td>1.065564</td>
      <td>0.995709</td>
      <td>71.265972</td>
    </tr>
    <tr>
      <th>133</th>
      <td>Domantas Sabonis</td>
      <td>IND</td>
      <td>24.42</td>
      <td>31.984065</td>
      <td>1.329774</td>
      <td>1.222974</td>
      <td>0.935912</td>
      <td>64.823166</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Ben Simmons</td>
      <td>PHI</td>
      <td>32.90</td>
      <td>39.960157</td>
      <td>1.235801</td>
      <td>1.136548</td>
      <td>0.975316</td>
      <td>64.486989</td>
    </tr>
    <tr>
      <th>42</th>
      <td>Bradley Beal</td>
      <td>WAS</td>
      <td>41.69</td>
      <td>47.880432</td>
      <td>1.169778</td>
      <td>1.075828</td>
      <td>0.990818</td>
      <td>63.614334</td>
    </tr>
    <tr>
      <th>245</th>
      <td>John Collins</td>
      <td>ATL</td>
      <td>18.46</td>
      <td>26.192835</td>
      <td>1.426170</td>
      <td>1.311629</td>
      <td>0.874687</td>
      <td>63.384272</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Anthony Davis</td>
      <td>LAL</td>
      <td>28.05</td>
      <td>35.397849</td>
      <td>1.273747</td>
      <td>1.171447</td>
      <td>0.957401</td>
      <td>62.465277</td>
    </tr>
    <tr>
      <th>424</th>
      <td>Rudy Gobert</td>
      <td>UTA</td>
      <td>12.11</td>
      <td>19.491754</td>
      <td>1.621689</td>
      <td>1.491445</td>
      <td>0.743980</td>
      <td>62.416989</td>
    </tr>
    <tr>
      <th>125</th>
      <td>Devin Booker</td>
      <td>PHX</td>
      <td>39.49</td>
      <td>45.710849</td>
      <td>1.177698</td>
      <td>1.083113</td>
      <td>0.988240</td>
      <td>62.065480</td>
    </tr>
    <tr>
      <th>444</th>
      <td>Stephen Curry</td>
      <td>GSW</td>
      <td>35.49</td>
      <td>41.270000</td>
      <td>1.210690</td>
      <td>1.113454</td>
      <td>0.981556</td>
      <td>61.780342</td>
    </tr>
    <tr>
      <th>239</th>
      <td>Jimmy Butler</td>
      <td>MIA</td>
      <td>30.16</td>
      <td>36.820908</td>
      <td>1.253294</td>
      <td>1.152637</td>
      <td>0.966403</td>
      <td>61.701542</td>
    </tr>
    <tr>
      <th>110</th>
      <td>DeMar DeRozan</td>
      <td>SAS</td>
      <td>31.95</td>
      <td>38.943015</td>
      <td>1.230290</td>
      <td>1.131480</td>
      <td>0.972531</td>
      <td>61.297541</td>
    </tr>
    <tr>
      <th>282</th>
      <td>Kawhi Leonard</td>
      <td>LAC</td>
      <td>35.24</td>
      <td>41.560621</td>
      <td>1.199544</td>
      <td>1.103204</td>
      <td>0.981029</td>
      <td>59.898776</td>
    </tr>
    <tr>
      <th>310</th>
      <td>Kyle Lowry</td>
      <td>TOR</td>
      <td>33.65</td>
      <td>39.849228</td>
      <td>1.212036</td>
      <td>1.114692</td>
      <td>0.977313</td>
      <td>59.430490</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Bam Adebayo</td>
      <td>MIA</td>
      <td>23.29</td>
      <td>30.257050</td>
      <td>1.319444</td>
      <td>1.213474</td>
      <td>0.927224</td>
      <td>58.093709</td>
    </tr>
    <tr>
      <th>73</th>
      <td>Chris Paul</td>
      <td>OKC</td>
      <td>30.27</td>
      <td>36.582512</td>
      <td>1.232470</td>
      <td>1.133485</td>
      <td>0.966816</td>
      <td>57.186114</td>
    </tr>
    <tr>
      <th>76</th>
      <td>Clint Capela</td>
      <td>ATL</td>
      <td>11.53</td>
      <td>18.265734</td>
      <td>1.608916</td>
      <td>1.479697</td>
      <td>0.726716</td>
      <td>53.481766</td>
    </tr>
    <tr>
      <th>221</th>
      <td>Jarrett Allen</td>
      <td>BKN</td>
      <td>9.21</td>
      <td>15.802198</td>
      <td>1.734327</td>
      <td>1.595036</td>
      <td>0.645207</td>
      <td>52.686162</td>
    </tr>
  </tbody>
</table>
</div>



Based on our new offensive score metric, these were the top 25 offensive players of the 2019-20 season. Note that a few of these players, like Steph Curry and Kyrie Irving missed a lot of games but had high scores the games they did play. Outside of that, I would say this is a pretty reasonable list, to make it to the top you need both volume and efficiency. I also believe playmaking is better rated in this metric than others by including assist opportunities, 2nd assists, and free throw assists.

What I like most about this metric is that volume at the cost of efficiency will hurt your score. For example, lets take an estimated Damian Lillard game where he has 42 NPTwAO and 52 PGen. Now let's say he continues to take 5 more shots, and makes 2 of them shooting 40% for 4 points, only producing .8 ppp. He would now have 47 NPTwAO and 56 PGen. Let's look at the difference in final scores between the two instances of the game.


```python
score = 52 ** ((52/42)/ppp) * (1 - 5 ** (-1*42 / npt_avg))
print('Score before shots', score)
score_final = 56 ** ((56/47)/ppp) * (1 - 5 ** (-1*47 / npt_avg))
print('Score after shots', score_final)
```

    Score before shots 89.14031151364419
    Score after shots 81.93279421061916


One flaw I have with PER, whose formula can be found [here], is that a player can improve their score with volume as long as they are shooting above 30.4% from the field. If I had a player shooting around 35%, I would not want him to increase his volume. My metric makes it so increasing volume is curved by the efficiency factor heavily so that volume is only good when they are producing above league average efficiency.

### Flaws

Now I will admit there are some flaws to this metric. Being a purely offensive stat focused metric, it leaves out stats like defensive rebounds, blocks, and steals which could lead to offensive possessions and may unfairly omit a good defender's actual contribution. It doesn't adjust for pace so plyers on teams that play faster might get more opportunities to generate points leading to higher scores. Using assist opportunities puts reliance on teammates to make shots, so a player's playmaking score might be a lot lower on a bad team than it would a good team, as you probably noticed there are only a few instances of a player on a bad team. I didn't really know how to go about this because leaving out unconverted opportunities misconstrues that player's usage, but if I were to try and regularize the conversion of assist opportunities it may unfairly punish those who set up their teammates better which is why their team is better in the first place.

This isn't really a flaw in the stat but another issue is that 2nd assists, free throw assists, and assist opportunities only go back to the 13-14 season when player tracking started so we will be unable to compare offensive scores historically unfortunately, unless we figure out a way to estimate these stats.

### Conclusion

I feel this is a good metric to compare offensive performances. This is not to show how skilled a player is necessarily as a lot of it is based on opportunity, but all the time we spend on comparing performance, I think this metric does a better job than most when it comes to offense. It can be used for single game matchups as well as whole seasons differentiating itself to metrics like offensive win shares, and in my opinion pretty unbiased to position.

While there are some flaws and can get a bit complicated, I believe this is a simpler metric to understand than other popular ones that get even more complicated, as it can be boiled down to pretty much volume affected by efficiency. A future task would be to figure out how to incorporate defense which can be extremely hard to measure in numbers.

[PER]: https://www.basketball-reference.com/about/per.html
[OWS]: https://www.basketball-reference.com/about/ws.html
[OBPM]: https://www.basketball-reference.com/about/bpm2.html
[nba.com/stats]: https://www.nba.com/stats/
[Python Script]: https://github.com/ckirch8/NBA_Player_Offense_Score/blob/main/off_eff_scrape.py
[github]: https://github.com/ckirch8/NBA_Player_Offense_Score/blob/main/offensive_efficiency_19_20.csv
[nba_api]: https://github.com/swar/nba_api
[here]: https://www.basketball-reference.com/about/per.html
