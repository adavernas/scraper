from datetime import date, datetime, timedelta
import pandas as pd 
import praw
import requests

config = {'limit': 1000,
          'replace_more': 10,
          'depth': 3,
          'exchange': 'S&P500'}

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
    df['count'] = df['count'] + [post.comments.list()[0].body.count(ticker) for ticker in df.ticker]
  


time.strftime('%s')

# config = {'limit':10,
#           'replace_more': 1,
#           'depth': 3,
#           'exchange': 'US'}
    
# config = {'columns': ['title','subreddit', 'selftext', 'num_comments', 'created_utc', 
#            'permalink', 'id'],
#           'limit':10,
#           'replace_more': 1,
#           'depth': 3,
#           'exchange': 'S&P500'}
# df = pd.DataFrame(columns=config['columns'])
# for post in subreddit.hot(limit=1):
#     dff = pd.DataFrame([[getattr(post, col) for col in config['columns']]], columns=config['columns'])
    
#     post.comments.replace_more(limit=config['replace_more'])
    
#     if config['depth']=='all':
#         dff['all_comments'] = ''.join(['\depth:' + str(post.comments.list()[i].depth) 
#                             + '\score:' + str(post.comments.list()[i].score)
#                             + '\ ' + post.comments.list()[i].body 
#                             for i in range(len(post.comments.list()))])
        
#     else:
#         all_comments = ''
#         comment_queue = post.comments[:]  # Seed with top-level
#         while comment_queue:
#             comment = comment_queue.pop(0)
#             all_comments = (all_comments + '\depth:' + str(comment.depth)
#                          + '\score:' + str(comment.score) + '\ ' + comment.body)
#             if comment.depth < config['depth']:
#                 comment_queue.extend(comment.replies)

#         dff['all_comments'] = all_comments
    
#     df = df.append(dff, ignore_index=True)



# def foo():            
# %load_ext line_profiler            
# %lprun -f foo foo()


# dff['all_comments'] = '\ '.join([post.comments.list()[i].body+' \depth:'
#        +str(post.comments.list()[i].depth) for i in range(len(post.comments.list()))])

# df['datetime'] = df['created_utc'].apply(lambda x: datetime.fromtimestamp(x))

# post.comments.replace_more(limit=None)
# cm = pd.DataFrame()
# for top_level_comment in post.comments:
#     cm = cm.append([top_level_comment.body],ignore_index=True)
    
# comment_queue = post.comments[:]  # Seed with top-level
# while comment_queue:
#     comment = comment_queue.pop(0)
#     print(comment.body)
#     comment_queue.extend(comment.replies)
 
# for comment in post.comments.list():
#     print(comment.body)
    
# post.comments.list()[i].body

# [post.comments.list()[i].body for i in range(5)]

# datetime.fromtimestamp(df['created'])

# df['created'].apply(lambda x: datetime.fromtimestamp(x))

# def get_date(created):
#     return dt.datetime.fromtimestamp(created)

# _timestamp = topics_data["created"].apply(get_date)

# topics_data = topics_data.assign(timestamp = _timestamp)

# topics_data.to_csv( os.path.join( os.getcwd(), '{}.csv'.format('wallstreetbets') ) , index=False)

# start_epoch=int((datetime.now() - timedelta(hours=36) ).timestamp())

# gen = PushshiftAPI().search_submissions(after=start_epoch,
#                              subreddit='wallstreetbets',
#                              limit=100)

# df = pd.DataFrame(columns=columns)
# for post in gen:
#     posts.append([post.title,  
#                   post.subreddit, 
#                   post.url, 
#                   post.num_comments, 
#                   post.selftext, 
#                   post.created,
#                   post.created_utc])

# columns = ['title','selftext']

# [{col: getattr(post, col)} for col in columns]

# pd.DataFrame({{'title': post.title},{'selftext': post.selftext}})

# pd.DataFrame([[getattr(post, col) for col in columns]], columns=columns)

# pd.DataFrame([getattr(post, col) for col in columns])




    
    


# start_epoch=int(dt.datetime(2017, 1, 1).timestamp())

# list(api.search_submissions(after=start_epoch,
#                             subreddit='politics',
#                             filter=['url', 'author', 'title', 'subreddit'],
#                             limit=10))


# import praw
# import pandas as pd
# import datetime as dt
# import os.path
# import pprint

# reddit = praw.Reddit(client_id='POr4MNjRuVfhFQ',
#                       client_secret='Ky91mxd6gavPlGeaWVa-C8avxGbCxg',
#                       user_agent='YOUR_APP_NAME',
#                       username='AAS-sudo',
#                       password='SHOF2020!')

# submission = reddit.submission(id="39zje0")
# print(submission.title)  # to make it non-lazy
# pprint.pprint(vars(submission))

# subreddit = reddit.subreddit('wallstreetbets')

# posts = []
# for post in subreddit.hot(limit=10000):
#     posts.append([post.title, 
#                   post.score, 
#                   post.id, 
#                   post.subreddit, 
#                   post.url, 
#                   post.num_comments, 
#                   post.selftext, 
#                   post.created])
    
# posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
# print(posts)

# def get_date(created):
#     return dt.datetime.fromtimestamp(created)

# _timestamp = posts["created"].apply(get_date)
# posts = posts.assign(timestamp = _timestamp)
    
# topics_dict = { "title":[], 
#                 "score":[], 
#                 "id":[], "url":[], \
#                 "comms_num": [], 
#                 "created": [], 
#                 "body":[]}
    
# for submission in df_subreddit:
#     topics_dict["title"].append(submission.title)
#     topics_dict["score"].append(submission.score)
#     topics_dict["id"].append(submission.id)
#     topics_dict["url"].append(submission.url)
#     topics_dict["comms_num"].append(submission.num_comments)
#     topics_dict["created"].append(submission.created)
#     topics_dict["body"].append(submission.selftext)
    
# topics_data = pd.DataFrame(topics_dict)

# def get_date(created):
#     return dt.datetime.fromtimestamp(created)

# _timestamp = topics_data["created"].apply(get_date)

# topics_data = topics_data.assign(timestamp = _timestamp)

# topics_data.to_csv( os.path.join( os.getcwd(), '{}.csv'.format('wallstreetbets') ) , index=False)

