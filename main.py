from flask import Flask, request, render_template_string
import mechanize
import json
import os
import time
from datetime import datetime
from time import sleep
import urllib.error

app = Flask(__name__)

g_headers = {
    'Connection': 'keep-alive',
    'authority': 'mbasic.facebook.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'www.google.com',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101"',
    'sec-ch-ua-full-version-list': '" Not A;Brand";v="99.0.0.0", "Chromium";v="101.0.4951.40"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua-platform-version': '"11.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
}

# Function to load cookies from file
def load_cookies_from_file(file_path, cookies):
    with open(file_path, 'r') as f:
        cookies_data = json.load(f)
        for key, value in cookies_data.items():
            c = mechanize.Cookie(
                version=0, name=key, value=value,
                port=None, port_specified=False,
                domain='facebook.com', domain_specified=True, domain_initial_dot=False,
                path='/', path_specified=True,
                secure=False, expires=None,
                discard=True, comment=None, comment_url=None, rest={}
            )
            cookies.set_cookie(c)

# Function to extract profile IDs from cookies
def extract_profile_ids(cookie_jar):
    profile_ids = []
    for cookie in cookie_jar:
        if cookie.name == 'c_user':
            profile_ids.append(cookie.value)
    return profile_ids

def openlink(browser, msg4):
    try:
        r = browser.open(msg4)
    except urllib.error.URLError:
        return None
    return r

def pawanXD(browser, comment):
    try:
        browser.select_form(nr=0)
        browser.form['comment_text'] = comment
        browser.submit()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Comment Done ✔ => [{current_time}]\n{comment}")
    except Exception as e:
        print(f"Error occurred while commenting: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_cookies = int(request.form.get('num_cookies'))
        cookie_files = request.form.getlist('cookie_files')
        post_link = request.form.get('post_link')
        notepad_file = request.form.get('notepad_file')
        time_interval = int(request.form.get('time_interval'))

        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        cookie_jars = []

        for cookie_file in cookie_files:
            cookies = mechanize.CookieJar()
            browser.set_cookiejar(cookies)

            for key, value in g_headers.items():
                browser.addheaders.append((key, value))

            load_cookies_from_file(cookie_file, cookies)

            profile_ids = extract_profile_ids(cookies)
            print(f"Loaded cookies for profiles: {profile_ids}")
            cookie_jars.append(cookies)

        with open(notepad_file, 'r') as f:
            lines = f.readlines()

        while True:
            try:
                for line in lines:
                    if len(line) > 3:
                        for cookies in cookie_jars:
                            browser.set_cookiejar(cookies)
                            if openlink(browser, post_link):
                                pawanXD(browser, line)
                                sleep(time_interval)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                continue
            sleep(1)

    form_html = '''
    <form method="POST">
        <label for="num_cookies">Number of Cookies:</label><br>
        <input type="number" name="num_cookies" required><br><br>

        <label for="cookie_files">Cookie Files (JSON paths):</label><br>
        <input type="text" name="cookie_files" required><br><br>

        <label for="post_link">Mbasic Post Link:</label><br>
        <input type="text" name="post_link" required><br><br>

        <label for="notepad_file">Notepad File Path:</label><br>
        <input type="text" name="notepad_file" required><br><br>

        <label for="time_interval">Time Interval (seconds):</label><br>
        <input type="number" name="time_interval" required><br><br>

        <input type="submit" value="Start">
    </form>
    '''
    return render_template_string(form_html)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
