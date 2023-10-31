import re
import uuid
import time
import requests
import logging
import argparse
from googletrans import Translator


class FlaskClient:
    def __init__(self, ip: str = '10.140.1.178', port: int = 37455, zh: bool = True, max_turns: int = 5, max_retry: int = 3):
        self.ip = ip
        self.port = port
        self.zh = zh
        self.max_turns = max_turns

        self.url_prefix_format = 'http://{}:{}/'
        self.url = self.url_prefix_format.format(self.ip, self.port)
        self.max_retry = max_retry
        self.translator = Translator()

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.handlers[0].setFormatter(logging.Formatter("%(message)s"))

    def _request(self, name: str, data: dict):
        for _ in range(self.max_retry):
            try:
                print(self.url, name, data)
                response = requests.post(self.url + name, json=data).json()
            except Exception as e:
                print('error', e)
                time.sleep(1)
                continue
            if response['code'] == 0:
                return response['ret']
            else:
                raise Exception(response['error_msg'])
        raise Exception("Web service failed. Please retry or contact with manager")

    def run(self, input_file: str):
        uid = uuid.uuid4().hex
        self.submit_posts(uid, input_file)

        count = 0
        while count < self.max_turns:
            question = self._request('get_question', {'uid': uid})['question']
            if self.zh:
                question_shown = self.translator.translate(question, src='en', dest='zh-tw').text + '\n'
            else:
                question_shown = question + '\n'
            question_shown = f'\n\033[32m[Q{count}] \033[0m' + question_shown + f'\033[32m[A{count}]\033[0m Your answer is: '

            pattern = re.compile('\([A-E]\)')
            while True:
                try:
                    answer = input(question_shown)
                except UnicodeDecodeError:
                    continue
                answer = answer.strip()
                if pattern.search(answer):
                    self._request('post_user_answer', {'uid': uid, 'answer': answer})
                    time.sleep(0.5)
                    break
                else:
                    self.logger.info("\033[31m[ERROR] Please input answer with proper format, such as: (A)\033[0m\n\n")
            count += 1
        result = self._request('get_final_result', {'uid': uid})['result']
        self.logger.info(f'\n\033[32m{result}\033[0m')
        return answer

    def submit_posts(self, uid: str, input_file: str):
        post_list = input_file.split('\n')
        post_list = [p for p in post_list if len(p) > 0 and not p.startswith('Possible MBTI')]
        self._request('post_user_posts', {'uid': uid, 'post_list': post_list})


if __name__ == "__main__":
    client = FlaskClient()
    client.run('i dont know')