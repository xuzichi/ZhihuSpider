"""
爬取topic中的question的answer部分
"""

import zhihu_login
import pandas
import json


class zhihuspider:

    def __init__(self, file_path, offset_i, question_id):
        account = zhihu_login.ZhihuAccount("", "")
        account.login(captcha_lang="en", load_cookies=True)
        response = self.get_response(0, question_id=question_id)
        dict_data = self.json_to_dict(response.text)
        result_list = []
        i = offset_i
        url, self.result_list = self.get_result(dict_data, result_list)
        while url:
            response = self.get_response(i, question_id=question_id)
            print(i)
            dict_data = self.json_to_dict(response.text)
            # print(dict_data)
            url, result_list = self.get_result(dict_data, self.result_list)
            i = i + offset_i
            self.save_to_excel(file_path)

    def get_response(self, offset, question_id):
        url = f"https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics"
        self.querystring = {
                            # "include": "data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics",
                            "limit": "5",
                            "offset": offset,
                            "sort_by": "default"
                            }
        account = zhihu_login.ZhihuAccount("", "")
        account.login(captcha_lang="en", load_cookies=True)
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
            if dict_data["paging"]["is_end"] is False:
                next_url = dict_data["paging"]["next"]
            else:
                next_url = None
            for one in dict_data["data"]:
                try:
                    if one["type"] == "answer":
                        one_info = {}
                        answer_id = one["id"]
                        content = one["content"]
                        author_name = one["author"]["name"]
                        voteup_count = one["voteup_count"]
                        comment_count = one["comment_count"]
                        one_info["answer_id"] = answer_id
                        one_info["content"] = content
                        one_info["author_name"] = author_name
                        one_info["voteup_count"] = voteup_count
                        one_info["comment_count"] = comment_count
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
    question_id = "362039517"
    file = "zhihu_answer.csv"
    zhihuspider(file_path=file, offset_i=5, question_id=question_id)
