#coding:utf-8
import re, json, datetime

MINUTE = 4

class CreateReplyText:
    log_root = "/home/hasegawa_chisato/reqanswer/nhk_programs/"
    dt = datetime.datetime.today()
    obj = None
    program_limit = 3

    @classmethod
    def read_json(self,fullpath):
        for line in open(fullpath,'r'):
            self.obj = json.loads(line)

    @classmethod
    def get_fullpath_for_itreration(self,itr,dt):
        path = self.log_root + dt.strftime("%Y/%m/%d/")
        filename = "program_" + dt.strftime("%Y-%m-%d") + "_" + itr + ".json"
        return path + filename

    @classmethod
    def grep_words_from_titles(self, words, service='a1'):
        return_strs = []
        program_count = 0
        service_list = ['g1','e1','s1']
        if service != 'a1':
            service_list = [service]
        for s in service_list:
            service_objs = self.obj['list'][s]
            for service_obj in service_objs:
                if self.will_be_on_air_from_time(service_obj['start_time']) and self.includes_all_word_in_title(service_obj,words):
                    program_count += 1
                    return_strs.append(service_obj['title'] + ' (' + s + ': ' + self.trim_time(service_obj['start_time'], service_obj['end_time']) + ')')
                    #print service_obj['title'] + ' (' + s + ': ' + self.trim_time(service_obj['start_time'], service_obj['end_time']) + ')'
                    if program_count >= self.program_limit:
                        return return_strs
        return return_strs

    @classmethod
    def includes_all_word_in_title(self, service_obj, words):
        for word in words:
            if re.search(word,service_obj['title']) is None and re.search(word,service_obj['subtitle']) is None:
                return False
        return True

    @classmethod
    def trim_time(self,start_time,end_time):
        start_list = self.split_date(start_time)
        end_list = self.split_date(end_time)
        program_time = start_list[0] + '/' + start_list[1] + '/' + start_list[2] + ' ' + start_list[3] + ':' + start_list[4] + '-' + end_list[3] + ':' + end_list[4]
#        program_time = start_list[3] + ':' + start_list[4] + '-' + end_list[3] + ':' + end_list[4]
        return program_time

    @classmethod
    def will_be_on_air_from_time(self,str_date):
        splited_date = self.split_date(str_date)
        splited_time_now = self.split_date(self.dt.strftime("%Y-%m-%d-%H-%M"))
        for i, now in enumerate(splited_time_now):
            if int(now) < int(splited_date[i]):
                return True
            elif int(now) > int(splited_date[i]):
                return False
        return True

    @classmethod
    def split_date(self, str_date):
        return re.split('[T\+\-:]',str_date)

    # not implemented for all area, but only Tokyo
    @classmethod
    def create_json_with_all_area(self,dt):
        fullpath = self.get_fullpath_for_itreration("130",dt)
        self.read_json(fullpath)

def main():
    crt = CreateReplyText()
    crt.create_json_with_all_area(self.dt)
    crt.grep_words_from_titles([u'アニメ'],'e1')

if __name__ == '__main__':
    main()