from datetime import datetime, timedelta
import pandas as pd 
import requests, praw, os

config = {'limit': 1000,
          'replace_more': 10,
          'depth': 3,
          'exchange': 'US',
          'hours': 24}
    
def count_ticker(text,score,ticker_list):
    return [((' ' + ticker) in text or (ticker + ' ') in text)*score for ticker in ticker_list]
    
if config['exchange']=='S&P500':
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = pd.DataFrame()
    df['ticker'] = table[0].Symbol
else:
    r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange='+config['exchange']+'&token=c0taruv48v6r4maeo8h0').json()
    list_tickers = [item['symbol'] for item in r]
    df = pd.DataFrame(list_tickers, columns=['ticker'])

wd = pd.read_csv(os.path.join(os.getcwd(), 'databases', 'common_words.txt'), delimiter = "\t", names=['words'])
wd = wd[wd.words.apply(lambda x: len(str(x))<=5)]
wd.words = wd.words.astype(str).str.upper()
wd = wd.reset_index(drop=True)

df = df[df.ticker.apply(lambda x: len(str(x))>1)]
df = df[ [not(wd.words.apply(lambda x: x==ticker).any()) for ticker in df.ticker] ]
df = df.reset_index(drop=True)

reddit = praw.Reddit(client_id='POr4MNjRuVfhFQ',
                     client_secret='Ky91mxd6gavPlGeaWVa-C8avxGbCxg',
                     user_agent='scraper',
                     username='AAS-sudo',
                     password='SHOF2020!')

subreddit = reddit.subreddit('wallstreetbets')
last_hours = (datetime.now() - timedelta(hours = config['hours']) - datetime(1970, 1, 1)).total_seconds()

df['count'] = 0
df['score'] = 0

df['comments'] = ''
text = df.set_index('ticker')['comments']
text = text.to_dict()
df = df.drop(columns='comments')

for post in subreddit.hot(limit=config['limit']):    
    post.comments.replace_more(limit=config['replace_more'])
    
    count_tik = count_ticker(post.title,1,df.ticker)
    df['count'] = df['count'] + count_tik
    for i, count in enumerate(count_tik):
        if count==1:
            text[df.ticker[i]] = text[df.ticker[i]] + '/b/' + post.title
            
    count_txt = count_ticker(post.selftext,1,df.ticker)
    df['count'] = df['count'] + count_txt
    for i, count in enumerate(count_txt):
        if count==1:
            text[df.ticker[i]] = text[df.ticker[i]] + '/b/' + post.selftext
            
    df['score'] = df['score'] + count_ticker(post.title,post.score,df.ticker)
    df['score'] = df['score'] + count_ticker(post.selftext,post.score,df.ticker)
                     
    for comment in post.comments.list(): 
        if comment.depth <= config['depth']:
            if comment.created_utc >= last_hours:
                count_tik = count_ticker(comment.body,1,df.ticker)
                df['count'] = df['count'] + count_tik
                df['score'] = df['score'] + count_ticker(comment.body,comment.score,df.ticker)
                for i, count in enumerate(count_tik):
                    if count==1:
                        text[df.ticker[i]] = text[df.ticker[i]] + '/b/' + comment.body
                                                  
df_name = '_'.join((config['exchange'],('h'+str(config['hours'])),str(datetime.today().year),str(datetime.today().month),str(datetime.today().day)))
   
df = df.sort_values(by=['count'],ascending=False)
             
df.to_csv(os.path.join(os.getcwd(), 'databases', '{}.csv'.format(df_name)), index=False)

f = open(os.path.join(os.getcwd(), 'databases', '{}.txt'.format(df_name)),"w")
f.write( str(text) )
f.close()

        
        
        
        
        