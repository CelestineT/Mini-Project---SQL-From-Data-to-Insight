import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import FileLink
from scipy.stats import pearsonr

roi_df = pd.read_csv(r'Data\Analysis\ROI per neighbourhood.csv')
comparison_df = pd.read_csv(r'Data\Analysis\ROI percent comparison.csv')
full_roi = pd.merge(left=roi_df, right=comparison_df, how='left', on='neighborhood').drop(['roi_percentage_y','borough_y'], axis=1)

house_costs_df = pd.read_csv(r'Data\Analysis\House cost per neighbourhood.csv')
house_market_share = pd.read_csv(r'Data\Analysis\House market share per neighbourhood.csv')
house_market_share = house_market_share.rename(columns={'neighborhood':'neighbourhood'})
full_house_market = pd.merge(left=house_costs_df, right=house_market_share, how='left', on='neighbourhood')

airbnb_revenue_df = pd.read_csv(r'Data\Analysis\Airbnb revenue per neighbourhood.csv')
airbnb_market_share = pd.read_csv(r'Data\Analysis\Airbnb market share per neighbourhood.csv')
airbnb_market_share = airbnb_market_share.rename(columns={'neighborhood':'neighbourhood'})
full_airbnb_market = pd.merge(left=airbnb_revenue_df, right=airbnb_market_share, how='left', on='neighbourhood')

full_market = pd.merge(left=full_house_market, right=full_airbnb_market, how='left', on='neighbourhood')
full_market.columns = [col.replace('_y','_airbnb').replace('_x','') for col in full_market.columns]
full_market = full_market.dropna()

def get_lolipop_plot(database,value_x, value_y,color_col, value_colorA, value_colorB ,colorA = 'purple', colorB = 'coral',):
    borough_colors = {
        value_colorA: colorA,
        value_colorB: colorB,
    }

    colors = database[color_col].map(borough_colors).fillna('gray')

    full_sorted = database.copy()
    full_sorted['color'] = colors
    full_sorted = full_sorted.sort_values(color_col, ascending=False)


    x = full_sorted[value_x]
    y = full_sorted[value_y]

    plt.figure(figsize=(14, 6))
    plt.vlines(x=x, ymin=0, ymax=y, colors=full_sorted['color'], alpha=0.8, linewidth=1)
    plt.scatter(x, y, color=full_sorted['color'], s=60, edgecolor='black', linewidth=0.5)

    plt.xticks(rotation=70, fontsize=9)
    plt.ylabel(input('Please enter label X'))
    plt.title(input('Please enter title'))
    plt.tight_layout()
    plt.show()

borough_colors = {
    'manhattan': 'purple',
    'brooklyn': 'coral',
}

sns.countplot(data=full_roi, x='market_saturation', hue='borough_x',palette=borough_colors)
plt.show()

borough_colors = {
    'manhattan': 'purple',
    'brooklyn': 'coral',
}

sns.countplot(data=full_roi, x='investment_tier', hue='borough_x',palette=borough_colors)
plt.show()

stack_data = full_roi.groupby(['market_saturation', 'borough_x']).size().unstack(fill_value=0)

# Plot stacked bar
stack_data.plot(
    kind='bar',
    stacked=True,
    figsize=(10, 6),
    color={
        'manhattan': 'purple',
        'brooklyn': 'coral',
    }
)

plt.title("Market Saturation by district")
plt.xlabel("Market Saturation")
plt.ylabel("Number of Listings")
plt.xticks(rotation=45)
plt.legend(title='Borough')
plt.tight_layout()
plt.show()

# Convert dataframe into series
l1 = full_market['avg_property_price']
l2 = full_market['avg_daily_price']

# Apply the pearsonr()
corr, _ = pearsonr(l1, l2)
x = full_market['avg_property_price']
y = full_market['avg_daily_price']

plt.scatter(x, y)

plt.show()
print(corr)

# Convert dataframe into series
l1 = full_market['neighborhood_share']
l2 = full_market['market_share_percent']

# Apply the pearsonr()
corr, _ = pearsonr(l1, l2)


x = full_market['neighborhood_share']
y = full_market['market_share_percent']

plt.scatter(x, y)

plt.show()
print(corr)

x = full_market['avg_daily_price']
y = full_market['market_share_percent']

plt.scatter(x, y)

plt.show()
print(corr)


x = full_market['neighbourhood']
y = full_market['avg_property_price']

# Define color map
borough_colors = {
    'manhattan': 'purple',
    'brooklyn': 'coral',
}
colors = full_market['borough_airbnb'].map(borough_colors).fillna('lightgray')

# Plot
plt.figure(figsize=(14, 6))
plt.bar(x, y, color=colors)

plt.xticks(rotation=70, fontsize=8)
plt.show()

brooklyn_data = full_market[full_market['borough_airbnb'] == 'brooklyn']


x = brooklyn_data['neighbourhood']
y = brooklyn_data['avg_property_price']

# Define color map
borough_colors = {
    'manhattan': 'purple',
    'brooklyn': 'coral',
}
colors = brooklyn_data['borough_airbnb'].map(borough_colors).fillna('lightgray')

# Plot
plt.figure(figsize=(14, 6))
plt.bar(x, y, color=colors)

plt.xticks(rotation=70, fontsize=8)
plt.show()