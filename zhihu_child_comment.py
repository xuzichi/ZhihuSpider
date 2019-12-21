"""
爬取topic中的comment的child_comment
"""

import zhihu_login
import pandas
import json


class zhihuspider:

    def __init__(self, file_path, offset_i, comment_id):
        account = zhihu_login.ZhihuAccount("", "")
        account.login(captcha_lang="en", load_cookies=True)
        response = self.get_response(0, comment_id=comment_id)
        dict_data = self.json_to_dict(response.content.decode('utf-8'))
        result_list = []
        i = offset_i
        url, self.result_list = self.get_result(dict_data, result_list)
        while url:
            response = self.get_response(i, comment_id=comment_id)
            print(i)
            dict_data = self.json_to_dict(response.content.decode('utf-8'))
            # print(dict_data)
            url, result_list = self.get_result(dict_data, self.result_list)
            i = i + offset_i
            self.save_to_excel(file_path)

    def get_response(self, offset, comment_id):

        url = f"https://www.zhihu.com/api/v4/comments/{comment_id}/child_comments"
        self.querystring = {
                            "limit": "20",
                            "offset": offset
                            }
        account = zhihu_login.ZhihuAccount("", "")
        account.login(captcha_lang="en", load_cookies=True)
        response = account.session.get(url, params=self.querystring)
        response.encoding = response.apparent_encoding
        return response

    def json_to_dict(self, json_data):
        dict_data = json.loads(json_data, encoding="utf_8")
        return dict_data

    def get_result(self, dict_data, result_list):
        if dict_data is None:
            next_url = None
            result_list = 0
        else:
            if dict_data["paging"]["is_end"] is False:
                next_url = dict_data["paging"]["next"]
            else:
                next_url = None
            for one in dict_data["data"]:
                try:
                    if one["type"] == "comment":
                        one_info = {}
                        child_comment_id = one["id"]
                        child_comment_content = one["content"]
                        one_info["child_conmment_id"] = child_comment_id
                        one_info["child_conmment_content"] = child_comment_content
                        result_list.append(one_info)
                        # print(one_info)
                except Exception as e:
                    pass
        return next_url, result_list

    def save_to_excel(self, file_path):
        df = pandas.DataFrame(self.result_list)
        df.to_csv(file_path, index=False, encoding="utf-8")
        print("save ok")


if __name__ == "__main__":
    comment_id = "573428773"
    file = "zhihu_child_comment.csv"
    zhihuspider(file_path=file, offset_i=20, comment_id=comment_id)
