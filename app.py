import tweepy

# Twitter API credentials
api_key = 'your api key'
api_secret = 'your api sec'
access_token = 'your acc tok'
access_token_secret = 'your acc tok sec'


# Authenticate
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Get recent 100 liked tweets
liked = api.get_favorites(count=100)
print(f"Found {len(liked)} liked tweets. Unliking...")

for tweet in liked:
    try:
        api.destroy_favorite(tweet.id)
        print(f"Unliked: {tweet.id}")
    except Exception as e:
        print(f"Error unliking tweet {tweet.id}: {e}")

# Get your own 100 most recent tweets/retweets
tweets = api.user_timeline(count=10, tweet_mode='extended', include_rts=True)
print(f"Found {len(tweets)} tweets. Undoing retweets...")

for tweet in tweets:
    # If it's a retweet, `retweeted_status` will exist
    if hasattr(tweet, 'retweeted_status'):
        try:
            api.unretweet(tweet.id)
            print(f"Unretweeted: {tweet.id}")
        except Exception as e:
            print(f"Error unretweeting {tweet.id}: {e}")


