from datetime import date, datetime, timedelta
import pandas as pd 
import praw, os, string
import requests

config = {'limit': 1000,
          'replace_more': 10,
          'depth': 3,
          'exchange': 'US'}

if config['exchange']=='S&P500':
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = pd.DataFrame()
    df['ticker'] = table[0].Symbol
else:
    r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange='+config['exchange']+'&token=c0taruv48v6r4maeo8h0').json()
    list_tickers = [item['symbol'] for item in r]
    df = pd.DataFrame(list_tickers, columns=['ticker'])

reddit = praw.Reddit(client_id='POr4MNjRuVfhFQ',
                     client_secret='Ky91mxd6gavPlGeaWVa-C8avxGbCxg',
                     user_agent='scraper',
                     username='AAS-sudo',
                     password='SHOF2020!')

subreddit = reddit.subreddit('wallstreetbets')

df['count'] = 0
for post in subreddit.hot(limit=config['limit']):    
    post.comments.replace_more(limit=config['replace_more'])
    df['count'] = df['count'] + [post.title.count(ticker) for ticker in df.ticker]
    df['count'] = df['count'] + [post.selftext.count(ticker) for ticker in df.ticker]
    for comment in post.comments.list(): 
        if comment.depth <= config['depth']:
            df['count'] = df['count'] + [comment.body.count(ticker) for ticker in df.ticker]

df_name = '_'.join((config['exchange'],str(datetime.today().year),str(datetime.today().month),str(datetime.today().day)))
                   
df.to_csv(os.path.join( os.getcwd(), 'database', '{}.csv'.format(df_name)), index=False)

df = df.sort_values(by=['count'])

df[df.ticker.str.len()>=3]