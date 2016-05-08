from requests import Request, Session


def login():
    post_data = {"source": "index_nav",
                 "form_email": "709933547@qq.com",
                 "form_password": "douban09933547"}
    url = "https://www.douban.com/accounts/login"
    sessions = Session()
    resp = sessions.post(url, post_data)
    print resp.status_code

    # resps = sessions.get("https://www.douban.com/")
    print resp.content


login()
