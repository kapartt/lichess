#!/usr/bin/python3
import json
import urllib.request
import os

s1 = 'Введите имя команды без пробелов и нажмите Enter'
s2 = 'Имя команды - это то, что написано в ссылке на страницу команды после https://lichess.org/team/'
s3 = 'Например, если ссылка имеет вид https://lichess.org/team/crestbook-chess-club'
s4 = 'То вы должны ввести crestbook-chess-club'
print(s1, s2, s3, s4, sep='\n')

team = input()

url = 'https://lichess.org/api/team/{0}/users'.format(team)

temp_dir = '{0}.json'.format(team)
csv_dir = '{0}.csv'.format(team)

if os.path.lexists(temp_dir):
    os.remove(temp_dir)
if os.path.lexists(csv_dir):
    os.remove(csv_dir)

print('Работаю...')
try:
    with open(temp_dir, 'wb') as f:
        with urllib.request.urlopen(url) as response:
            s = response.read()
            f.write(s)

    variants = ['chess960', 'antichess', 'puzzle', 'atomic', 'racingKings', 'blitz', 'crazyhouse',
                'threeCheck', 'bullet', 'correspondence', 'classical', 'rapid']
    head_str = 'player;' + ';'.join(variants)

    with open(temp_dir, 'r', encoding='utf-8') as f:
        with open(csv_dir, 'w') as f_csv:
            print(head_str, file=f_csv)

            for ln in f.readlines():
                player = json.loads(ln)
                p_str = [player['id']]
                for x in variants:
                    perf = player['perfs'].get(x, None)
                    if perf is None:
                        p_str.append('1500')
                    else:
                        p_str.append(str(player['perfs'][x]['rating']))
                print(';'.join(p_str), file=f_csv)

    os.remove(temp_dir)
    print('Готово!')
except urllib.request.HTTPError:
    print('Команды с таким именем не существует.')
    os.remove(temp_dir)
finally:
    input()


