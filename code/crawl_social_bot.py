import botometer
from io_utils import *
from tqdm import tqdm


def crawl_social_bot():
    start, end = 4990, 6990
    print("Start {} end {}".format(start, end))
    entities = load_text_as_list("entities.txt")
    users = [int(u[5:]) for u in entities if u.startswith("user_")][start:end]
    output_path = "bot_{}_{}.json".format(start, end)

    # rapidapi_key = "192d74943amsh2b2e43ba0cf2ab3p12dd32jsn97c3f50370ec"
    # twitter_app_auth = {
    #     'consumer_key': 'jYdmX6aHKPj7FGnkLsj2askNowG3frUzDZegvGLwlaNnmvRSkB',
    #     'consumer_secret': 'fYfQlgZtRZtBHJ28sdxShaJ1qoABcTklfW5GONiZTE93BXI4Vd',
    #     'access_token': '1107472618972577792-7pPChHKtnZzgUEamRxeHCPSowXmXik',
    #     'access_token_secret': 'gwa5a9pHIrze3RddcHnCKXEmHkjpxwkAcTGibFzNfCcTE',
    # }
    # rapidapi_key = "d6ed745814msheb2918d2f53d126p149910jsnef5971d324e1"
    # twitter_app_auth = {
    #     'consumer_key': 'm26PgTCMHkeQft9TJquv6XeFG',
    #     'consumer_secret': 'jYdmX6aHKPj7FGnkLsj2askNowG3frUzDZegvGLwlaNnmvRSkB',
    #     'access_token': '1107472618972577792-z4PbLiNXSwUcaD1lu2y8hMX2vxZCTV',
    #     'access_token_secret': 'q4Kau7f299Fn0CfVhzklSYLzRlpJERKuk83kT2cNLMqIW',
    # }
    # rapidapi_key = "192d74943amsh2b2e43ba0cf2ab3p12dd32jsn97c3f50370ec"
    # twitter_app_auth = {
    #     'consumer_key': 'zOWhsXSpGyInSoiLesdopTm8k',
    #     'consumer_secret': 'v5p2XVPaL3hjEfbOMQBHjM38VE3fEVzakzdiFlpsjds0cXxT0R',
    #     'access_token': '1192760967538462720-ssHe0X6DLgjIHOFvZ9hNXl5byPPIoh',
    #     'access_token_secret': 'mLFejqoBCmyUh0DvgTyrWBJWYV0YmrRgvq9DV1p3zT13C',
    # }
    rapidapi_key = "6123048600msh23d6f41ae6efeffp1188b7jsn7f9e93ab44e0"
    twitter_app_auth = {
        'consumer_key': 'Hqfik7AcuOR8cCX0WmySgnqTe',
        'consumer_secret': 'yuOWc9p0bpyZKWWucx6qDlawDejX17fV6s2eIxHjqYxwNvPHK9',
        'access_token': '1192760967538462720-Wk4UU9fJA9sNbqyOiY5y1i9Tyof6Io',
        'access_token_secret': 'rtKuP20PxEusX5mQi69XqglQW01sq2hZLKK2jBf3eCV2D',
    }
    bom = botometer.Botometer(wait_on_ratelimit=True,
                              rapidapi_key=rapidapi_key,
                              **twitter_app_auth)
    user_bot_scores = {}
    for user in tqdm(users, desc="Crawling users"):
        try:
            result = bom.check_account(user)
            bot_score = result["display_scores"]["universal"]
        except Exception as e:
            print(e)
            bot_score = -1
        user_bot_scores[user] = bot_score
    save_json(user_bot_scores, output_path)


if __name__ == "__main__":
    crawl_social_bot()