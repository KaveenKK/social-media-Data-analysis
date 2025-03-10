import pandas as pd
#loading each dataset
df_insta_overview = pd.read_csv(r"Instagram_Profile_Overview.csv")
df_insta_post_engagement = pd.read_csv(r"Instagram_Post_Engagement.csv")
df_insta_demographics = pd.read_csv(r"Instagram_Age_Gender_Demographics.csv")
df_insta_top_cities = pd.read_csv(r"Instagram_Top_Cities_Regions.csv")

# Check the first few rows
print(df_insta_overview.head())
print(df_insta_post_engagement.head())
print(df_insta_demographics.head())
print(df_insta_top_cities.head())

#loading each dataset
df_fb_overview = pd.read_csv(r"Facebook_Profile_Overview.csv")
df_fb_post_engagement = pd.read_csv(r"Facebook_Post_Engagement.csv")

# Check the first few rows
print(df_fb_overview.head())
print(df_fb_post_engagement.head())

"""Check for missing values"""

#print(df_insta_overview.isnull().sum())
print(df_insta_post_engagement.isnull().sum())
#print(df_fb_overview.isnull().sum())
#print(df_fb_post_engagement.isnull().sum())

"""As there are no missing values in instagram post engagement data sheet, we can go for further analysis.

Check for duplicates
"""

print(df_insta_post_engagement.duplicated().sum())
#print(df_fb_post_engagement.duplicated().sum())

"""We can now drop unneccessary column for the analysis"""

df_insta_post_engagement = df_insta_post_engagement.drop(columns=['Video views', 'RowHash'])

print(df_insta_post_engagement.head())

"""Now we need to seperate feed posts from the reels, in order to find the instgram posts average engagement rate."""

print(df_insta_post_engagement.dtypes)

"""• Calculate the average engagement rate for Instagram posts.

average Engagement Rate= (Total Engagement of all posts/Total Reach of all posts)* 100
# New section
​
Here, we will be diving the total engagement by reach instead of total followers. the reason is public instagram accounts will often be shown to non followers. Hence, it will be more accurate to divide by the numbwer of reach.

Let's Find the engagment of each post as a percentage
"""

df_insta_post_engagement['Engagement Rate'] = (
    df_insta_post_engagement['Like count'] +
    df_insta_post_engagement['Comments count'] +
    df_insta_post_engagement['Shares']+
     df_insta_post_engagement['Unique saves']
) / df_insta_post_engagement['Media reach']

#Engagment rate for each post as a percentage
print("Average Engagement Rate for Each Instagram Post (%):")
#displaying post engagament as a percentage value
df_insta_post_engagement['Engagement Rate'] = df_insta_post_engagement['Engagement Rate'].apply(lambda x: round(x, 3) * 100)
print(df_insta_post_engagement['Engagement Rate'])

#Downloading the updated csv file for future analysis in PowerBI
df_insta_post_engagement.to_csv('instagram_post_engagement_with_avg.csv', index=False)

"""Now lets find the average engagment rate of the total posts for instagram."""

# average engagement rate for all Instagram posts
average_engagement_rate = df_insta_post_engagement['Engagement Rate'].mean()

# Print the average engagement rate
print("Average Engagement Rate for Instagram Posts:", average_engagement_rate)
# Print the average engagement rate as a percentage
print("Average Engagement Rate for Instagram Posts (%):", average_engagement_rate * 100)

"""
• Identify the top-performing post based on engagement (likes, comments, shares)."""

# Find the top performing post based on engagement rate
top_insta_post = df_insta_post_engagement.nlargest(1, 'Engagement Rate')

# Print the details of the top post
print(top_insta_post[['Date', 'Media ID', 'Media product type', 'Media caption',]])
print(f"Engagement Rate: {top_insta_post['Engagement Rate'].values[0] * 100:.2f}%")

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

#size of the plot
plt.figure(figsize=(20,5))
#X and Y axis labels
sns.lineplot(data=df_insta_post_engagement, x='Date', y='Engagement Rate')
plt.xticks(rotation=45)
plt.title("Instagram Engagement Rate Over Time")

# Format y-axis as percentage
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))  # 1.0 is represented multiplying by 100


plt.show()

"""Plot a bar chart comparing different post types (Reels vs. Static Posts).

Lets Compare the Avergae engagament rate for Feed posts and Reel Posts.
"""

# Grouping data by 'Media product type' and calculating the average engagement rate
average_engagement_by_type = df_insta_post_engagement.groupby('Media product type')['Engagement Rate'].mean()

# The average engagement rate for each post type
print(average_engagement_by_type)

"""Now lets see it in a bar graph"""

# bar plot to compare average engagement rates
plt.figure(figsize=(7, 5))
sns.barplot(x=average_engagement_by_type.index, y=average_engagement_by_type.values)
plt.title("Average Engagement Rate by Post Type (Instagram)")
plt.ylabel("Average Engagement Rate")
plt.xlabel("Post Type")
plt.show()

"""Write a function that predicts whether a post will perform well based on previous
engagement data (e.g., using a simple threshold model).

Here, We would define a well performing post as getting high amount of reach. Let's find out if the post will be performing well when it has more engagement.
"""

def predict_post_performance(engagement_data, threshold):
  """Predicts whether a post will perform well based on engagement data.

  Args:
    engagement_data: A pandas DataFrame containing engagement data for previous posts.
    threshold: The engagement rate threshold above which a post is considered
      to perform well.

  Returns:
    A pandas Series containing predictions (True for good performance, False
    otherwise).
  """

  # Calculate the average engagement rate for previous posts
  average_engagement_rate = engagement_data['Engagement Rate'].mean()

  # Create a Series of predictions based on the threshold
  predictions = engagement_data['Engagement Rate'] > threshold * average_engagement_rate

  return predictions

"""Here, we can change the threshold value based on how we want to define a successful post. If a certain post is higher than the benchmark set, it will show as a well performing post(TRUE)"""

predictions = predict_post_performance(df_insta_post_engagement, threshold=0.5)

df_insta_post_engagement['Predicted Performance'] = predictions
print(df_insta_post_engagement[['Date', 'Media caption', 'Predicted Performance']])
