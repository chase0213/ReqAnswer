#coding:utf-8
import twitter
from create_reply_text import *

class ReqAnswer:

    api = None
    last_tweet_id_file = '.last_tweet_id'

    @classmethod
    def __init__(self,filename):
        tokens = []
        for line in open(filename,'r'):
            tokens.append(line.replace('\n',''))
        self.api = twitter.Api(tokens[0],tokens[1],tokens[2],tokens[3])

    @classmethod
    def tweet_test(self,msg):
       self.api.PostUpdate(status=msg)

    @classmethod
    def reply_to_tweet_id(self,tid,msg):
        try:
            return self.api.PostUpdate(status=msg,in_reply_to_status_id=tid)
        except:
            print 'could not reply to the tweet, may not be any programs', tid

    @classmethod
    def get_my_timeline(self,since_id=0):
        return self.api.GetHomeTimeline(since_id=since_id)

    @classmethod
    def get_hashed_tweets(self,timeline,target_tag):
        hashed_list = []
        for tweet in timeline:
            hashtags = tweet.hashtags
            for hashtag in hashtags:
                if hashtag.text.lower() == target_tag:
                    hashed_list.append(tweet)
                    # break not to include the same tweet
                    break
        return hashed_list

    @classmethod
    def reply_to_hashed_tweets(self):
        ltid = self.read_last_tweet_id()
        if ltid == '':
            ltid = 0

        # refollows before get timeline
        self.refollow()
        timeline = self.get_my_timeline(ltid)

        # remembers the latest tweet id
        if timeline != []:
            self.write_last_tweet_id(str(timeline[0].GetId()))
        
        # gets a list of tweets include hash tag "nhk_reqanswer"
        hashed_list = self.get_hashed_tweets(timeline,'nhk_reqanswer')
        
        # replies to the tweets
        crt = CreateReplyText()
        # the target programs are today's and tomorrow's
        dts = [datetime.datetime.today(),datetime.datetime.today() + datetime.timedelta(days=1)]

        for dt in dts:

            # reads json file
            if not crt.create_json_with_all_area(dt):
                return False

            # extracts tweet from the list
            for tweet in hashed_list:

                # creates text to reply
                words = self.get_tweet_text_as_list(tweet)
                service, words = self.remove_unuse_texts(words)
                #print service, words[0]
                msg_list = crt.grep_words_from_titles(words,service=service)
                msg = '@' + tweet.user.screen_name
                for body in msg_list:
                    msg = msg + ' ' + body

                # if there are no programs, replies to the tweet with a message no programs found
                if msg_list == []:
                    msg = msg + ' ' + 'no programs with'
                    for word in words:
                        msg = msg + ' ' + word

                self.reply_to_tweet_id(tweet.GetId(),msg)

        return True

    @classmethod
    def remove_unuse_texts(self,words):
        clean_words = []
        service = ''
        for word in words:
            if re.search('^[#@].*',word) is None:
                if word in ['-G','-E','-S','-g','-e','-s','-A','-a']:
                    service = word[1].lower() + '1'
                else:
                    clean_words.append(word)
        if service == '':
            service = 'a1'
        return service, clean_words

    @classmethod
    def get_tweet_text_as_list(self,tweet):
        return re.split('[\s\"\']',tweet.GetText())

    @classmethod
    def read_last_tweet_id(self):
        last_id = 0
        for tweet_id in open(self.last_tweet_id_file,'r'):
            if tweet_id != 'None':
                last_id = int(tweet_id)
            return last_id

    @classmethod
    def write_last_tweet_id(self,tid):
        f = open(self.last_tweet_id_file,'w')
        f.write(tid)
        f.close()

    @classmethod
    def follow(self,user):
        try:
            self.api.CreateFriendship(user)
        except:
            pass

    @classmethod
    def refollow(self):
        try:
            followers = self.api.GetFollowers()
        except:
            print 'could not get followers, may not be authenticated.'
        for follower in followers:
            user = follower.screen_name
            self.follow(user)

def main():
    ra = ReqAnswer('.twitter_tokens')
    ra.reply_to_hashed_tweets()

if __name__ == '__main__':
    main()
