"""
爬取topic中的answer的comment部分
"""

import zhihu_login
import pandas
import json


class zhihuspider:

    def __init__(self, file_path, offset_i, answer_id):
        account = zhihu_login.ZhihuAccount("", "")
        account.login(captcha_lang="en", load_cookies=True)
        response = self.get_response(0, answer_id=answer_id)
        dict_data = self.json_to_dict(response.content.decode('utf-8'))
        result_list = []
        i = offset_i
        url, self.result_list = self.get_result(dict_data, result_list)
        while url:
            response = self.get_response(i, answer_id=answer_id)
            print(i)
            dict_data = self.json_to_dict(response.content.decode('utf-8'))
            # print(dict_data)
            url, result_list = self.get_result(dict_data, self.result_list)
            i = i + offset_i
            self.save_to_excel(file_path)

    def get_response(self, offset, answer_id):

        url = f"https://www.zhihu.com/api/v4/answers/{answer_id}/root_comments"
        self.querystring = {
                            "limit": "10",
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
                        comment_id = one["id"]
                        comment_content = one["content"]
                        comment_author_name = one["author"]["member"]["name"]
                        comment_vote_count = one["vote_count"]
                        child_comment_count = one["child_comment_count"]
                        one_info["comment_id"] = comment_id
                        one_info["comment_content"] = comment_content
                        one_info["comment_author_name"] = comment_author_name
                        one_info["comment_vote_count"] = comment_vote_count
                        one_info["child_comment_count"] = child_comment_count
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
    answer_id = "837548419"
    file = "zhihu_comment.csv"
    zhihuspider(file_path=file, offset_i=10, answer_id=answer_id)
