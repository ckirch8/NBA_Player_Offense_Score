
# Total Offense Score

The goal of this article is to create a new metric to judge a single player's offensive production. I know there is a ton out there already ([PER], [OWS], [OBPM], etc.) but I wanted to try my hand at creating one and possibly find ways improve upon them. My metric will mostly be based on total production and how efficient that player was at achieving that production.


### Results




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




[PER]: https://www.basketball-reference.com/about/per.html
[OWS]: https://www.basketball-reference.com/about/ws.html
[OBPM]: https://www.basketball-reference.com/about/bpm2.html
[nba.com/stats]: https://www.nba.com/stats/
[Python Script]: https://github.com/ckirch8/NBA_Player_Offense_Score/blob/main/off_eff_scrape.py
[github]: https://github.com/ckirch8/NBA_Player_Offense_Score/blob/main/offensive_efficiency_19_20.csv
[nba_api]: https://github.com/swar/nba_api
[here]: https://www.basketball-reference.com/about/per.html
