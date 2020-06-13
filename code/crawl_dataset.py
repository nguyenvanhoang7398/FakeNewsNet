from crawl_tweet_ids import init_twython
from news_content_collection import crawl_news_article
from urllib import request, error
from tqdm import tqdm
from io_utils import *
from collections import Counter
from twython import exceptions
import preprocessor as p


def crawl_status_source(twitter, tweet_id):
    source_urls, source_titles, clean_text = [], [], ""
    try:
        status = twitter.show_status(id=tweet_id)
        clean_text = p.clean(status['text'])
        status_urls = status['entities']['urls']
        for source_url in status_urls:
            full_url = source_url['expanded_url']
            try:
                response = request.urlopen(full_url, timeout=10)
                news_article = crawl_news_article(response.url)
                if news_article is not None:
                    source_urls.append(news_article['canonical_link'])
                    source_titles.append(news_article['title'])
            except Exception as e:
                print(e)
                continue
    except exceptions.TwythonError as e:
        print(e)
    return source_urls, source_titles, clean_text


def crawl_sources(twitter_path):
    twitter_content = read_csv(twitter_path, True, ",")
    header = twitter_content[0]
    output_content = []
    twitter = init_twython()
    default_url, default_title = "PLEASE_ENTER_URL", "PLEASE_ENTER_TITLE"

    for row in tqdm(twitter_content, desc="Crawling {}".format(twitter_path)):
        if len(row[1]) == 0 or row[1] == default_url or len(row[2]) == 0 or row[2] == default_title:
            tweet_ids = row[3].split("\t")
            all_source_urls, all_source_titles, all_tweet_text = [], [], []
            for tweet_id in tqdm(tweet_ids, desc="Iterating tweets"):
                source_urls, source_titles, clean_text = crawl_status_source(twitter, tweet_id)
                all_source_urls.extend(source_urls)
                all_source_titles.extend(source_titles)
                all_tweet_text.append(clean_text)
            if len(all_source_urls) > 0 and len(all_source_titles) > 0:
                most_common_title = Counter(all_source_titles).most_common()[0][0]
                most_common_url = Counter(all_source_urls).most_common()[0][0]
            else:
                if len(all_tweet_text) > 0:
                    # set the title to be most common text status
                    most_common_title = Counter(all_tweet_text).most_common()[0][0]
                else:
                    most_common_title = default_title
                most_common_url = "https://twitter.com/"
            output_content.append([row[0], most_common_url, most_common_title.replace(",", ""), row[3]])
        else:
            output_content.append(row)

    output_path = twitter_path.replace(".csv", "_crawled.csv")
    write_csv(output_content, header, output_path, delimiter=",")


if __name__ == "__main__":
    crawl_sources("fakenewsnet_dataset/twitter/twitter_fake_annot.csv")
    crawl_sources("fakenewsnet_dataset/twitter/twitter_real_annot.csv")

