import csv
import threading
import tkinter as tk
from tweety import Twitter
import time

def run_twitter_extraction():
    global user_entry, pages_entry

    user = user_entry.get()
    pages = int(pages_entry.get())

    cookies_value = """guest_id=guest_id_value;"""
    app = Twitter("session")
    app.load_cookies(cookies_value)
    print(app.me)

    tweets = app.get_tweets(username=user, pages=pages, wait_time=1)

    csv_file = open('tweets.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Tweet Time', 'Tweet Link', 'Tweet Body', 'Is Retweet'])

    if tweets:
        for tweet in tweets:
            if hasattr(tweet, 'tweets') and tweet.tweets: 
                tweet_info_time = str(tweet.tweets[0].created_on)
                tweet_info_link = str(tweet.tweets[0].id)
                tweet_info_link_final = f"https://twitter.com/{user}/status/{tweet_info_link}"
                time.sleep(1)
                tweet_detail = app.tweet_detail(tweet_info_link_final)
                csv_writer.writerow([tweet_info_time, tweet_info_link_final, tweet_detail.tweet_body, tweet_detail.is_retweet])
            else:
                tweet_info_time = str(tweet.created_on)
                tweet_info_link = str(tweet.id)
                tweet_info_link_final = f"https://twitter.com/{user}/status/{tweet_info_link}"
                time.sleep(1)
                tweet_detail = app.tweet_detail(tweet_info_link_final)
                csv_writer.writerow([tweet_info_time, tweet_info_link_final, tweet_detail.tweet_body, tweet_detail.is_retweet])

        csv_file.close()
        print("Los tweets se han guardado correctamente en 'tweets.csv'")
    else:
        print("No se encontraron tweets para el usuario", user)

def start_extraction():
    thread = threading.Thread(target=run_twitter_extraction)
    thread.start()

def create_interface():
    global user_entry, pages_entry

    root = tk.Tk()
    root.title("Extracción de Tweets")

    user_label = tk.Label(root, text="Usuario:")
    user_label.pack()
    user_entry = tk.Entry(root)
    user_entry.pack()

    pages_label = tk.Label(root, text="Número de páginas:")
    pages_label.pack()
    pages_entry = tk.Entry(root)
    pages_entry.pack()

    start_button = tk.Button(root, text="Extracer tweets", command=start_extraction)
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_interface()
