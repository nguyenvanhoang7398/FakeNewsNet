from io_utils import *


def build_coaid():
    fake_news = "../dataset/coaid_fake_news.csv"
    fake_tweets = "../dataset/coaid_fake_tweets.csv"
    fake_replies = "../dataset/coaid_fake_replies.csv"
    real_news = "../dataset/coaid_real_news.csv"
    real_tweets = "../dataset/coaid_real_tweets.csv"
    real_replies = "../dataset/coaid_real_replies.csv"

    fake_news = read_csv(fake_news, False, ",")
    fake_tweets = read_csv(fake_tweets, False, ",")
    fake_replies = read_csv(fake_replies, False, ",")
    real_news = read_csv(real_news, False, ",")
    real_tweets = read_csv(real_tweets, False, ",")
    real_replies = read_csv(real_replies, False, ",")

    header = ["id", "news_url", "title", "tweet_ids"]

    for news, tweets, replies, label in [(fake_news, fake_tweets, fake_replies, "fake"),
                                (real_news, real_tweets, real_replies, "real")]:
        tweet_map = {}

        for row in tweets:
            index, tweet_id = row
            if index not in tweet_map:
                tweet_map[index] = set()
            tweet_map[index].add(tweet_id)

        for row in replies:
            index, tweet_id, reply_id = row
            if index not in tweet_map:
                tweet_map[index] = set()
            tweet_map[index].add(tweet_id)
            tweet_map[index].add(reply_id)

        data = []
        for row in news:
            if label == "fake":
                index, news_type, fact_check_url, archieve, news_url, news_url2, news_url3, news_url4, news_url5, \
                    title, newstitle, content, abstract, publish_date, meta_keywords = row
            elif label == "real":
                index, news_type, fact_check_url, news_url, title, newstitle, content, abstract, publish_date, \
                    meta_keywords = row
                news_url2, news_url3, news_url4, news_url5 = "", "", "", ""
            else:
                raise ValueError("Unsupported label {}".format(label))
            if news_type == "article":
                if index in tweet_map:
                    tweet_idxs = tweet_map[index]
                else:
                    print("No engagement for article {}".format(index))
                    tweet_idxs = ""
                if len(news_url) > 0:
                    final_news_url = news_url
                elif len(news_url2) > 0:
                    final_news_url = news_url2
                elif len(news_url3) > 0:
                    final_news_url = news_url3
                elif len(news_url4) > 0:
                    final_news_url = news_url4
                elif len(news_url5) > 0:
                    final_news_url = news_url5
                else:
                    final_news_url = ""

                if len(title) > 0:
                    final_news_title = title
                elif len(newstitle) > 0:
                    final_news_title = title
                else:
                    final_news_title = ""

                data.append(["coaid_{}_{}".format(label, index), final_news_url, final_news_title, " ".join(tweet_idxs)])

        write_csv(data, header, "../dataset/coaid_{}.tsv".format(label), "\t")


if __name__ == "__main__":
    build_coaid()