import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
sns.set()

data = pd.read_csv('output.csv')

# columns for reference
#   ['Target Points', 'Player Won?', 'Player Tied?', 'Player Busted?',
#    'Player Points', 'Dealer Points', 'Dealer Showing', 'Player Points on Last Hit',
#    'Decks', 'Points Array']

# # get the average wins, ties, and losses per target points
# avg_df = data[['Target Points', 'Player Won?']].groupby(by=['Target Points']).mean()
# avg_df['Player Tied?'] = data[['Target Points', 'Player Tied?']].groupby(by=['Target Points']).mean()
# avg_df['Player Lost?'] = 1 - (avg_df['Player Won?'] + avg_df['Player Tied?'])

# create bar plot
ax1 = sns.barplot(x='Target Points', y='Player Won?', data=data, color='dodgerblue')
ax1.set(ylabel="Probability of Winning")

# getting target points and dealer showing for permutations
target_points = data['Target Points'].unique()
dealer_showing = sorted(data['Dealer Showing'].unique())

# creating target point matrix for heatmap
target_matrix = pd.DataFrame(columns=dealer_showing, index=target_points)
for showing in dealer_showing:
    target_matrix[showing] = data.loc[data['Dealer Showing'] == showing].groupby('Target Points')['Player Won?'].mean()

# print(target_matrix)

fig, ax = plt.subplots(figsize=(10, 6))
ax = sns.heatmap(target_matrix, annot=True, fmt=".2f", linewidths=0.4, ax=ax)
ax.set(xlabel='Dealer Points Showing', ylabel='Player Target Points', title='Probability of Winning')
fig.savefig("winning_probability.png");
