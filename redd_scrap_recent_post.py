import requests
import pandas as pd
import csv


# print(dir(requests))

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('USE_SCRIPT', 'SECRET')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'YOUR_USER',
        'password': 'YOUR_PASS'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'YOUR_BOT'}


# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
# print(res)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']


# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get("https://oauth.reddit.com/r/pics/hot",
                   headers=headers)

df = pd.DataFrame()  # initialize dataframe

# loop through each post retrieved from GET request
for post in res.json()['data']['children']:
    # append relevant data to dataframe
    df = df._append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }, ignore_index=True)

# df.to_csv('reddit_posts.csv', index=False)
#
# print("CSV file exported successfully.")

print(df.head())
