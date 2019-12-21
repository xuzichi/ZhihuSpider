"""
用于爬取问题关注数，被浏览数，问题的本体和内容，问题的提出者
"""

from lxml import etree
import pandas

import zhihu_login

question_id = "35670502"
f = open('question.html', 'w', encoding='utf-8')
result_list = []
one_info = {}
account = zhihu_login.ZhihuAccount('', '')
account.login(captcha_lang='en', load_cookies=True)

url = f"https://www.zhihu.com/question/{question_id}"
response = account.session.get(url)
f.write(response.text)
html = etree.parse('question.html', etree.HTMLParser())
result = html.xpath('//*[@class="NumberBoard-itemValue"]/@title')
one_info["关注者"] = result[0]
one_info["被浏览"] = result[1]
print('关注者：' + result[0])  # 关注者
print('被浏览：' + result[1])  # 被浏览

url = "https://zhihu-web-analytics.zhihu.com/api/v2/za/logs/batch"
response = account.session.post(url)
f.write(response.text)
html = etree.parse('question.html', etree.HTMLParser())
result = html.xpath('//*[@class="QuestionHeader-title"]/text()')
one_info["question_title"] = result[0]
print(result[0])  # 问题主体
result = html.xpath('//*[contains(@class, "QuestionRichText")]/div/span/text()')
one_info["question_content"] = result[0]
print(result[0])  # 问题详细内容

url = f"https://www.zhihu.com/question/{question_id}/log"
response = account.session.get(url)
f.write(response.text)
html = etree.parse('question.html', etree.HTMLParser())
result_name = html.xpath('//*[@class="zm-item"]/div[1]/a/text()')
result_href = html.xpath('//*[@class="zm-item"]/div[1]/a/@href')
result_auth = result_name[len(result_name) - 1]
one_info["auth"] = result_auth
result_href = ['https://www.zhihu.com' + i for i in result_href]
result_auth_href = result_href[len(result_href) - 1]
one_info["auth_href"] = result_auth_href
print(result_name)  # 问题提出者与后续编辑者
print(result_href)  # 问题提出者和后续编辑者的个人地址
print(result_auth)  # 问题提出者
print(result_auth_href)  # 问题提出者的个人地址

result_list.append(one_info)
df = pandas.DataFrame(result_list)
df.to_csv('zhihu_question_info.csv', index=False, encoding='utf-8')
print("save ok")
