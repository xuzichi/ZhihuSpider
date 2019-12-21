"""
爬取设定topic部分，从test部分转移至此
"""

import zhihu_login
import pandas
import json


class zhihuspider:

    def __init__(self, search_key, file_path, offset_i):
        account = zhihu_login.ZhihuAccount('', '')
        account.login(captcha_lang='en', load_cookies=True)
        response = self.get_response(search_key, 0)
        dict_data = self.json_to_dict(response.text)
        result_list = []
        i = offset_i
        url, self.result_list = self.get_result(dict_data, result_list)
        while url:
            response = self.get_response(search_key, i)
            print(i)
            # f = open('zhihu.html', 'w', encoding='utf-8')
            # f.write(response.text)
            # f2 = open('www.txt', 'w')
            # f2.write(url)
            dict_data = self.json_to_dict(response.text)
            print(dict_data)
            url, result_list = self.get_result(dict_data, self.result_list)
            i = i + offset_i
            self.save_to_excel(file_path)

    def get_response(self, search_key, offset):
        url = 'https://www.zhihu.com/api/v4/search_v3'
        self.querystring = {"t": "topic",
                            "q": search_key,  # 需要什么话题只需要把参数传到这里就行
                            "correction": "1",
                            "offset": offset,
                            "limit": "20",
                            "show_all_topics": "1",
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
                    if one['type'] == 'search_result':
                        one_info = {}
                        title = one['highlight']['title'].replace("<em>", "").replace("</em>", "").strip()
                        question_id = one["object"]['id']
                        # print(question_id)
                        description = one["object"]['excerpt'].replace("<em>", "").replace("</em>", "").strip() + "..."
                        href = f"http://www.zhihu.com/topic/{question_id}/hot"
                        one_info['url'] = href
                        one_info['title'] = title
                        one_info['description'] = description
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
    search = '你好'
    file = 'zhihu_topic.csv'
    zhihuspider(search_key=search, file_path=file, offset_i=20)
