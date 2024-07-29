import requests, wget, os, time, random
from audioplayer import AudioPlayer
from colorama import init, Fore
init(autoreset=True)
c1 = 0

def replaces(var):
    var = var.replace('!','%21')
    var = var.replace('\"', '%22')
    var = var.replace('#', '%23')
    var = var.replace('$', '%24')
    var = var.replace('&', '%26')
    var = var.replace('\'', '%27')
    var = var.replace('(', '%28')
    var = var.replace(')', '%29')
    var = var.replace('*', '%2A')
    var = var.replace('+', '%2B')
    var = var.replace('/', '%2F')
    return var

def login():
    global c1, acs_tkn, rfr_tkn, uid
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.MAGENTA + "Введите почту или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 2
        elif mail.count('@') == 1:
            pw = input(Fore.MAGENTA + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={replaces(pw)}").json()
                if 'data' in lrqst:
                    if lrqst['code'] == 0:
                        if 'totp_session_token' in lrqst['data']:
                            tfa = ''
                            while True:
                                while tfa == "":
                                    tfa = input('Введите код 2FA:')
                                else:
                                    auth2 = requests.get(f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                    if auth2['code'] == 0:
                                        c1 = 1
                                        acs_tkn = auth2['data']['access_token']
                                        rfr_tkn = auth2['data']['refresh_token']
                                        uid = auth2['data']['user_id']
                                        return acs_tkn, rfr_tkn, uid
                                    else:
                                        print(Fore.RED + 'Ошибка')
                                        tfa = ''
                        else:
                            c1 = 1
                            acs_tkn = lrqst['data']['access_token']
                            rfr_tkn = lrqst['data']['refresh_token']
                            uid = lrqst['data']['user_id']
                            return acs_tkn, rfr_tkn, uid

                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')

def main():
    menu = int(input('Выберите действие: \n 1 - Создать бота \n 2 - Обновить токен \n'))
    if menu == 1:
        nick  = str(input('Отлично. Теперь введите имя будущего бота(должно заканчиваться на "bot"):'))
        if nick.endswith('bot'):
            createBot = requests.get(f'https://monopoly-one.com/api/bots.create?access_token={acs_tkn}&nick={nick}').json()
            #print(createBot)
            if createBot['code'] == 191:
                print(Fore.RED+'Электронная почта на аккаунте не подтверждена')
                input()
                exit()
            elif createBot['code'] == 1802:
                print(Fore.RED+'Низкая статистика профиля(должно быть не менее 500 побед на профиле, зарегистрированном не менее 3 месяцев назад)')
                input()
                exit()
            elif createBot['code'] == 0:
                botUid = createBot["data"]["user_id"]
                print(Fore.GREEN+f'Успешно создан бот {nick}. m1.gg/{botUid}')
                ipCheck = str(input('Введите 0, если будете управлять ботом с данного устройства или введите ip другого устройства:'))
                if ipCheck == '0':
                    getBotToken = requests.get(f'https://monopoly-one.com/api/bots.getToken?access_token={acs_tkn}&user_id={botUid}').json()['data']['access_token']
                else:
                    getBotToken = requests.get(f'https://monopoly-one.com/api/bots.getToken?access_token={acs_tkn}&user_id={botUid}&ip={ipCheck}').json()['data']['access_token']
                print(Fore.GREEN+f'Токен вашего бота: {getBotToken}')
            else:
                print(Fore.RED+'Произошла непредвиденная ошибка')
                input()
                exit()
        else:
            print(Fore.RED + 'Ошибка. Неверный формат данных')
            input()
            exit()
    elif menu == 2:
        botUid = int(input('Отлично. Теперь введите user_id вашего бота:'))
        ipCheck = str(input('Введите 0, если будете управлять ботом с данного устройства или введите ip другого устройства:'))
        if ipCheck == '0':
            getBotToken = requests.get(f'https://monopoly-one.com/api/bots.getToken?access_token={acs_tkn}&user_id={botUid}').json()['code']
            if getBotToken == 0:
                botToken = getBotToken['data']['access_token']
            else:
                print(Fore.RED+'Такого бота не существует')
                input()
                exit()
        else:
            getBotToken = requests.get(f'https://monopoly-one.com/api/bots.getToken?access_token={acs_tkn}&user_id={botUid}&ip={ipCheck}').json()['code']
            if getBotToken == 0:
                botToken = getBotToken['data']['access_token']
            else:
                print(Fore.RED+'Такого бота не существует')
                input()
                exit()

        print(Fore.GREEN+f'Токен вашего бота: {botToken}')

print(Fore.LIGHTWHITE_EX + 'BotControl. Made by AssKiss Studio. https://github.com/AssKissStudio/M1BotControl')
login()
main()
