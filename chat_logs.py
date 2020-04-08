import requests, json
from pathlib import Path

class KakaoChatLogs:
  baseUrl = ''
  cookies = ''

  chat_id = ''
  session = None

  file_index = 0

  def __init__(self, chat_id, cookies):
    self.baseUrl = 'https://center-pf.kakao.com/api/profiles/{profile_id}}/chats/{}/chatlogs'.format(chat_id)
    self.chat_id = chat_id
    self.session = requests.Session()
    self.cookies = cookies
    self.session.cookies.set('sessionid', self.cookies)

  def fetch(self, last = None, direction=None):
    print('fetch, chat_id: {}'.format(self.chat_id))
    if last is None and direction is None:
      res = self.session.get(self.baseUrl)
    else:
      res = self.session.get('{}?since={}&direction={}'.format(self.baseUrl, last, direction))
    jsonRes = json.loads(res.text)

    try:
      last_chat_id = jsonRes['items'][0]['id']
    except IndexError:
      last_chat_id = None
    
    has_prev = jsonRes.get('has_prev', None)
    has_next = jsonRes.get('has_next', None)

    Path("chatlogs/{}".format(self.chat_id)).mkdir(parents=True, exist_ok=True)
    self.save('chatlogs/{}/{}.dat'.format(self.chat_id, self.file_index), res.text)
    self.file_index += 1

    if has_prev is True:
      self.fetch(last_chat_id, 'backward')
  
  def save(self, file_name, data):

    with open(file_name, 'w') as f:
      f.write(data)
