import requests
from bs4 import BeautifulSoup
import json

r = requests.get('https://www.gktoday.in')
c = r.content

soup = BeautifulSoup(c, 'html.parser')
topic = soup.find_all('li', {'class': 'sidebar'})
data = []
for x in topic:
    n = 0
    link = x.find('a').get('href')
    heading = x.text
    while n<11:
        w = [link+'?pageno='+str(n)]
        for y in w:
            r1 = requests.get(y)
            c1 = r1.content

            soup1 = BeautifulSoup(c1, 'html.parser')
            qus = soup1.find_all('div', {'class': 'sques_quiz'})
            for i in qus:
                d = {}
                qus = i.find('div', {'class': 'wp_quiz_question testclass'}).text.replace('\n', '').replace('\xa0', '').replace('\u2018', '').replace('\u2019', '').strip().split('.')
                d['qus'] = qus[1]
                try:
                    option = i.find('div', {'class': 'wp_quiz_question_options'}).text.replace('\n           ', '').replace('\u2013', '')
                except:
                    continue
                op = option.split('[')
                d['op1'] = op[1].replace('A]', '').strip()
                d['op2'] = op[2].replace('B]', '').strip()
                d['op3'] = op[3].replace('C]', '').strip()
                d['op4'] = op[4].replace('D]', '').strip()
                answer = i.find('div', {'class': 'ques_answer'}).text.replace('\n           ', '').replace('Correct Answer: ', '').split(' ')
                d['answer'] = answer[0]
                data.append(d)
        #print(data)
        n+=1
    allqus = {}
    allqus['topic'] = heading
    allqus['data'] = data
    try:
        json_object = json.dumps(allqus, indent=4)
        with open(str(heading)+'.json', "w") as file:
            file.write(json_object)
    except:
        continue
    # df = pandas.DataFrame(allqus)
    # df.to_json(heading+'mcq.json')
