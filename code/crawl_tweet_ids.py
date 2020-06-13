import argparse
from twython import Twython
import time
import random
from io_utils import *
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description='Graph Learning')
    parser.add_argument('--input-path', type=str, default="../dataset/news.tsv", help='input news file path')
    parser.add_argument('--output-path', type=str, default="../dataset/corona_fake.tsv", help='output news file path')
    return parser.parse_args()


def init_twython():
    json_object = json.load(open("config.json"))
    app_key, app_secret, oauth_token, oauth_token_secret = None, None, None, None

    with open(json_object["tweet_keys_file"], 'r') as fKeysIn:
        next(fKeysIn)
        for line in fKeysIn:
            line = line.rstrip().split(',')

            app_key, app_secret, oauth_token, oauth_token_secret = line[0], line[1], line[2], line[3]

    client_args = {'timeout': 30, 'verify': False}

    return Twython(app_key=app_key, app_secret=app_secret, oauth_token=oauth_token,
                   oauth_token_secret=oauth_token_secret, client_args=client_args)


def crawl_tweet_ids(twitter, input_path, output_path):
    news_info = read_csv(input_path, False, "\t")
    exported_news_info = []
    for row in tqdm(news_info, desc="Crawling tweet ids"):
        news_id = row[0]
        url = row[1]
        claim = row[2]
        result = twitter.search(q=claim, count=100)
        tweet_ids = []
        if "statuses" in result:
            for tweet in result["statuses"]:
                tweet_ids.append(str(tweet["id"]))
        time.sleep(random.uniform(1, 5))
        exported_news_info.append([news_id, url, claim, " ".join(tweet_ids)])
    write_csv(exported_news_info, ["id", "news_url", "title", "tweet_ids"], output_path, "\t")


if __name__ == "__main__":
    p_args = parse_args()
    twitter_obj = init_twython()
    crawl_tweet_ids(twitter_obj, p_args.input_path, p_args.output_path)
