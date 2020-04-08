import requests, json

class KakaoChannel:
  # 카카오 채널에 있는 채팅리스트를 가져온다.
  
  baseUrl = 'https://center-pf.kakao.com/api/profiles/{profile_id}/chats/search'
  session = None

  cookies = ''
  file_index = 0
  
  def __init__(self, cookies):
    self.session = requests.Session()
    self.cookies = cookies
    self.session.cookies.set('sessionid', self.cookies)
    

  def fetch(self, last = None):
    if last is None:
      res = self.session.post(self.baseUrl)
    else:
      res = self.session.post('{}?since={}'.format(self.baseUrl, last))

    has_next = json.loads(res.text)['has_next']
    last_log_id = json.loads(res.text)['items'][-1]['last_log_id']

    self.save('search/{}_{}.dat'.format(self.file_index, last_log_id), res.text)
    self.file_index += 1
    if has_next:
      self.fetch(last_log_id)

  def save(self, file_name, data):
    with open(file_name, 'w') as f:
      f.write(data)


with open('cookies.dat', 'r') as f:
  instant_cookies = f.read()
  Kakao = KakaoChannel(instant_cookies)
  Kakao.fetch()