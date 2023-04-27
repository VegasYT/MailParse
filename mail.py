import imaplib
import email
import time
from email.header import decode_header


# Задаем параметры подключения к почтовому серверу
host = "imap.mail.ru"
username = "login@mail.ru"
password = 'pass(для внешних приложений)'

print('Проверка почты, пока сообщений нет. Ждем...')
while True:
    # Подключаемся к почтовому серверу
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)

    # Выбираем папку "входящие сообщения"
    mail.select('inbox')
    # Ищем сообщения
    _, search_data = mail.search(None, 'UNSEEN')  # Ищем только непрочитанные сообщения

    # Получаем id сообщений
    msg_ids = search_data[0].split()

    # Если сообщений нет, ждем
    if not msg_ids:
        time.sleep(3)  # Ждем 5 секунд и проверяем заново
        continue
    # Если сообщение есть, получаем его содержимое
    msg_id = msg_ids[-1]  # Берем последнее сообщение из списка
    _, msg_data = mail.fetch(msg_id, '(RFC822)')


    # Извлекаем текст письма из данных
    raw_email = msg_data[0][1]
    # Извлекаем содержимое сообщения
    raw_msg = msg_data[0][1]
    msg = email.message_from_bytes(raw_msg)

    # Получаем отправителя
    sender = msg['from']

    # Преобразуем данные в объект класса EmailMessage
    email_message = email.message_from_bytes(raw_email)
    # Извлекаем электронный адрес отправителя
    email_from = email_message["from"]
    name, email_addr = email.utils.parseaddr(email_from)


    # Получаем текст сообщения
    if msg.is_multipart():
        # Если сообщение содержит несколько частей, ищем текстовую часть
        for part in msg.get_payload():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('utf-8')
                break
    else:
        # Если сообщение содержит только текст, то берем его
        body = msg.get_payload(decode=True).decode('utf-8')

    # заголовок темы письма
    subject_header = msg['Subject'];
    # декодирование темы письма
    decoded_subject = email.header.decode_header(subject_header)[0][0].decode('utf-8')



    MessText = body
    MessAdr = email_addr
    MessTopic = decoded_subject

    print("\nПРИШЛО НОВОЕ ПИСЬМО:\n" + "От: " + MessAdr + "\nТема письма: " + MessTopic + "\nТекст письма: " + MessText)



# Закрываем соединение
mail.close()
mail.logout()
