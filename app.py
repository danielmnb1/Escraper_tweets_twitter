import csv
from tweety import Twitter
import time

cookies_value = """guest_id=guest_id_value; guest_id_marketing=guest_id_marketing; guest_id_ads=guest_id_ads; kdt=kdt_value; auth_token=auth_token_value; ct0=ct0_value; twid=twid_value; personalization_id="personalization_id_value" """

# Cookies can be a str or a dict

app = Twitter("session")
app.load_cookies(cookies_value)
print(app.me)

#recuerden que las limitaciones de tweeter son muchas , solo se puede una cantidad por Hora
user = 'elonmusk'
pages= 5
tweets = app.get_tweets(username=user, pages=pages, wait_time=1)

csv_file = open('tweets.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Tweet Time', 'Tweet Link', 'Tweet Body', 'Is Retweet'])

if tweets:
    for tweet in tweets:
        if hasattr(tweet, 'tweets') and tweet.tweets: 
            tweet_info_time = str(tweet.tweets[0].created_on)
            tweet_info_link = str(tweet.tweets[0].id)
            tweet_info_link_final=f"https://twitter.com/{user}/status/{tweet_info_link}"
            time.sleep(1)
            tweet_detail = app.tweet_detail(tweet_info_link_final)
            csv_writer.writerow([tweet_info_time, tweet_info_link_final, tweet_detail.tweet_body, tweet_detail.is_retweet])
        else:
            tweet_info_time = str(tweet.created_on)
            tweet_info_link = str(tweet.id)
            tweet_info_link_final=f"https://twitter.com/{user}/status/{tweet_info_link}"
            time.sleep(1)
            tweet_detail = app.tweet_detail(tweet_info_link_final)
            csv_writer.writerow([tweet_info_time, tweet_info_link_final, tweet_detail.tweet_body, tweet_detail.is_retweet])

    csv_file.close()
    print("Los tweets se han guardado correctamente en 'tweets.csv'")
else:
    print("No se encontraron tweets para el usuario", user)
