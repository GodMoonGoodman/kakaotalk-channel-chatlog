import json
from chat_logs import KakaoChatLogs
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('chats') if isfile(join('chats', f))]
sorted_files = sorted(onlyfiles, key=lambda file: int(file.split('_')[0]))

with open('cookies.dat', 'r') as c:
  cookies = c.read()

# 각 채팅의 id값을 리스트로 저장
whole_chats = []

for dat_file in sorted_files:
  with open('chats/{}'.format(dat_file), 'r') as f:
    data = json.loads(f.read())
    whole_chats += data['items']


count = 0
for chat in whole_chats:
    print('count : {}'.format(count))
    count += 1
    chat = KakaoChatLogs(chat['id'], cookies)
    chat.fetch()
