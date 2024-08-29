import requests


def send_sms(phone_number, sms_text):
    smsc_login = "nianatoliy87"
    smsc_password = "nmnmnm888Ni@"
    encoded_message = requests.utils.quote(sms_text)  # кодируем сообщение
    url = f"https://smsc.kz/sys/send.php?login={smsc_login}&psw={smsc_password}&phones={phone_number}&mes={encoded_message}"

    response = requests.get(url)

    if response.status_code == 200:
        response_text = response.text
        if response_text.startswith("OK"):
            return response_text
        else:
            raise Exception(f"Отправка SMS не удалась. Ответ сервера: {response_text}")
    else:
        raise Exception(f"Отправка SMS не удалась с кодом статуса {response.status_code}")
