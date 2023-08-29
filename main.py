import requests
import random
import string
import time
import os

API = 'https://www.1secmail.com/api/v1/'
domain_list = ["1secmail.com", "1secmail.org", "1secmail.net"]
domain = random.choice(domain_list)


def generate_username():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username


def check_mail(mail=''):
    req_link = f'{API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
    r = requests.get(req_link).json()
    length = len(r)

    if length == 0:
        print('[INFO] нет новых сообщений (~5с)')
    else:
        id_list = []

        for i in r:
            for k, v in i.items():
                if k == 'id':
                    id_list.append(v)

        print(f'[+] {length} входящих (~5с)')

        current_dir = os.getcwd()
        final_dir = os.path.join(current_dir, 'all_mails')

        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        for i in id_list:
            read_msg = f'{API}?action=readMessage&login={mail.split("@")[0]}&domain={mail.split("@")[1]}&id={i}'
            r = requests.get(read_msg).json()

            sender = r.get('from')
            subject = r.get('subject')
            date = r.get('date')
            content = r.get('textBody')
            body = r.get('body')

            mail_file_path = os.path.join(final_dir, f'{i}.txt')

            with open(mail_file_path, 'w') as file:
                file.write(f'from: {sender}\n'
                           f'mail: {mail}\n'
                           f'subject: {subject}\n'
                           f'date: {date}\n'
                           f'content: {content}\n'
                           f'body: {body}\n')


def delete_mail(mail=''):
    url = 'https://www.1secmail.com/mailbox'

    data = {
        'action': 'deleteMailbox',
        'login': mail.split('@')[0],
        'domain': mail.split('@')[1]
    }

    r = requests.post(url, data=data)
    print(f'[X] почтовый адрес {mail} удален!\n')


def main():
    try:
        username = generate_username()
        mail = f'{username}@{domain}'
        print(f'[+] почтовый адрес:\n{mail}')

        mail_req = requests.get(f'{API}?login={mail.split("@")[0]}&domain={mail.split("@")[1]}')

        while True:
            check_mail(mail=mail)
            time.sleep(5)

    except KeyboardInterrupt:
        delete_mail(mail=mail)
        print('[!] программа прервана')


if __name__ == '__main__':
    main()
