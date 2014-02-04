#coding:utf-8
import twitter

class ReqAnswer:

    api = None

    @classmethod
    def __init__(self,filename):
        tokens = []
        for line in open(filename,'r'):
            tokens.append(line.replace('\n',''))
        self.api = twitter.Api(tokens[0],tokens[1],tokens[2],tokens[3])

    @classmethod
    def tweet_test(self,msg):
       self.api.PostUpdate(status=msg)

def main():
    ra = ReqAnswer('.twitter_tokens')
    ra.tweet_test('test')

if __name__ == '__main__':
    main()
