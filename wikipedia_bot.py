from requests_html import HTMLSession
import os
import praw
import prawcore
import re
from record import CommentRecord

def login():
    """ logs into Reddit account """
    return praw.Reddit(client_id=os.environ.get('REDDIT_CID'), 
                       client_secret=os.environ.get('REDDIT_SECRET'),
                       user_agent='test wikipedia bot script',
                       username=os.environ.get('REDDIT_USER'),
                       password=os.environ.get('REDDIT_PASS'))

def get_wikiurl(comment): 
    """ returns wikipedia url if comment has it, otherwise returns None """
    # match = re.search('[https://]?en.wikipedia.org/wiki/.+', comment)
    if comment is None:
        return comment

    match = re.search('en.wikipedia.org/wiki/[^\)\s\[\]\\\\]*', comment)
    if match:
        return 'https://' + match.group()
    return None

def get_paragraph(url):
    """ returns first paragraph from given url """
    session = HTMLSession()
    r = session.get(url)
    if r.status_code != 200:
        return None
    para = r.html.find('p', first=True)
    para_str = remove_brackets(para.text)
    return para_str

def remove_brackets(text):
    return re.sub('\[.*?\]', '', text)

def reply_wiki(sub, st):
    for comment in subreddit.stream.comments():
        if not st.contains(comment):
            url = get_wikiurl(comment.body)
            if url:
                para = get_paragraph(url)
                if para:                    # quickfix
                    try:
                        comment.reply(para)
                    except prawcore.exceptions.Forbidden as e:
                        print(e, url)
                        st.save_comments()
                    except praw.exceptions.APIException as e:
                        print(e, e.message)
                        st.save_comments()
            st.add_comment(comment)

if __name__ == '__main__':
    reddit = login()
    subreddit = reddit.subreddit('all')
    st = CommentRecord()                           # used to keep track of seen comments

    try:
        reply_wiki('all', st)
    except KeyboardInterrupt:
        print('exception detected and comment ids saved')
        st.save_comments()