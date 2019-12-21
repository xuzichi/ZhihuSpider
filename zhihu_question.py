"""
爬取topic中的questons部分
"""

import zhihu_login
import pandas
import json


class zhihuspider:

    def __init__(self, file_path, offset_i, topic_id):
        account = zhihu_login.ZhihuAccount('', '')
        account.login(captcha_lang='en', load_cookies=True)
        response = self.get_response(0, topic_id=topic_id)
        dict_data = self.json_to_dict(response.text)
        result_list = []
        i = offset_i
        url, self.result_list = self.get_result(dict_data, result_list)
        while url:
            response = self.get_response(i, topic_id=topic_id)
            print(i)
            dict_data = self.json_to_dict(response.text)
            print(dict_data)
            url, result_list = self.get_result(dict_data, self.result_list)
            i = i + offset_i
            self.save_to_excel(file_path)

    def get_response(self, offset, topic_id):
        url = f'https://www.zhihu.com/api/v4/topics/{topic_id}/feeds/timeline_question'
        self.querystring = {
                            "include": "data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;",
                            "limit": "10",
                            "offset": offset,
                            }
        account = zhihu_login.ZhihuAccount('', '')
        account.login(captcha_lang='en', load_cookies=True)
        response = account.session.get(url, params=self.querystring)
        response.encoding = response.apparent_encoding
        return response

    def json_to_dict(self, json_data):
        dict_data = json.loads(json_data, encoding="utf_8_sig")
        return dict_data

    def get_result(self, dict_data, result_list):
        if dict_data is None:
            next_url = None
            result_list = 0
        else:
            if dict_data['paging']['is_end'] is False:
                next_url = dict_data['paging']['next']
            else:
                next_url = None
            for one in dict_data['data']:
                try:
                    if one['target']['type'] == 'question':
                        one_info = {}
                        title = one['target']['title'].strip()
                        print(title)
                        question_id = one["target"]['id']
                        print(question_id)
                        href = f"http://www.zhihu.com/question/{question_id}"
                        one_info['url'] = href
                        one_info['title'] = title
                        result_list.append(one_info)
                        # print(one_info)
                except Exception as e:
                    pass
        return next_url, result_list

    def save_to_excel(self, file_path):
        df = pandas.DataFrame(self.result_list)
        df.to_csv(file_path, index=False, encoding='utf-8')
        print("save ok")


if __name__ == '__main__':
    topic_id = '20848505'
    file = 'zhihu_question.csv'
    zhihuspider(file_path=file, offset_i=10, topic_id=topic_id)
