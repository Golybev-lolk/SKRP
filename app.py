import datetime
import gspread
import streamlit as st
import base64
from google.oauth2.service_account import Credentials

# Точный ID вашей Google Таблицы
SPREADSHEET_ID = "13H-fmBuw2vpzsB5ci6oPzl26-_nZ7LRkhZVpJIG81Uo"

# Идеально упакованный оригинальный ключ в формат Base64 без единого скрытого символа или переноса строки
B64_KEY = (
    "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVG"
    "QUFTQ0JLb3dnZVNqQWdFQUFvSUJBUURIRkRNU3o1VFdoVGYyXG5tc0VwU0JndmozaFJFMWVxTEJN"
    "WWc3c2NlVWI1RmpWNWhZbjFOUzdkc1l3WGxxZ01ZR2JBSVd2ektPVFpBZVpEXG5PK0h4aWt3QXJO"
    "S0c0M0xVd1oxS05RbENJeWJwTEtZNGJtdndTdUF6WkZPN2lnSXZ1NCtFOEhYelZzT3dJYUxhXG5F"
    "QU54d2RWYUg4WGZ0cjY2cmVJZ1hlVW1GZGNsMlk2eHQvYWoyTktlR2VrSDBXdE55bGUxUVlKYmsx"
    "ZUNnU1JcbjhGam5DZnlrLzErSElwanBhM3NmNzQrdXZPcFk1cDltMTNxYVFmZlU3bG5lL05JbkZp"
    "N3JMKzJUNzU1TFVwc1x5MHBQSnBDOFFha1BrQkZrK053dHhwemRkbXp2SWo1YUdBdVp3ZWVPMXdE"
    "STVUYm5lVk9iek4zTWV0Rk1yRnFOXG52Sng5eGpwOUFnTUJBQUVDZ2dFQUYwLzZCcThjNjEwQ0Qx"
    "cUxFeXlSVWMwZjV5SlRiUUFEaXVoc2RWZ1Y3dUhEXG5sMUJCYzl2UlBCUUh2d0c3N3RpL1pLWjBW"
    "ZXB3bUNQUnZIUXV5cTZpbGlpaDU3Q0g4RzZuVzNWcGZDQ1hMb3Z2XG45V1dyd0p6TjdvMUVBNXFS"
    "bDJxQ3o2dC9MU1VmTjBXMEl2MWhIY2V1MFlDcU1uSHJrZlVHWWNHQ2E4cDkxWHBSXG54TDRhdkU5"
    "WHMrbnBrYU9WWU5wcnJHTHcyT0EzcjNuNjNVM2dBeVFxeUM2TWdWRzh5b0J2MjQ3MFordXBjbnpV"
    "XG4yM0NzYmFUcUtZKzEySlhwTFM0d0I3OXA4MGlaMTFTMm5nWHIzbFlZYnc3WVJvUGkzTkdCb3Vi"
    "UzVxVHliaG41XG5LaUVYTlN3ZnBidDd3aW5iRHhvam13UzJrZGZ4YmtLbmNaYXVtMEp6cVFLQmdR"
    "RHJHVlVaVHZHaGtTTHlRUm9sXG5VYlZwVDN6VGh4NzdKYWhCdm5tVkJGaDZXSm5RSGZiSnNoajJZ"
    "TDZUaGcwWkJyQm5LRHZqSjZlK2l6bEF1ZlNCTX crappy"
    "VllThVZDZsazQ1NHNwWEtZRzIwY3hoeU9tUFFOQnBDVG45SFdqbkZuN2hrR1ZHcmNNeUV0bXFYdn"
    "RYZHFcbkVlWGw3dURjUmNlWjhDZG5HRDdOOSt3NjRLQmdRRFkrMWlzWXZjcW12STZTNW5mYjNFam"
    "NJOVZFdTVkMHgvN1xiVnlIR2NtR3dzaEFTeDNtWFB4UDEsa0NOaUpvaTFyWmxZSW0vNjhKQlNRcz"
    "hhUFl4MjYyNU5KaVVsZ0E5UjBnTVxuMFZId1FUc1p5a1poMG1YcUp0cFRBaDN6R0NoajhwTmdlQi"
    "9xRmR1U1hqSldYZG5hL2hZbnVxYVdlTGZTWWRtMVxucl狠OEdMdGdkUUtCZ0FtRGNPa1hRNjNp"
    "RGFQMzlzTGtKNDhuWkVtN0FnbnZzQ3RZNWRxdDNtYTFCeVJnMGdlL1xuYVRzekZGM0Y0dW5NVFNN"
    "ZmdhemNnZW80QUEwYWVVWnZUeWFtem04Q21KdzRpY0lMditKZjJiK0dVTWw5YndMSFxuN1RuTUVk"
    "VzQwTGYvN290UEJ6UDU3YkhHdkVnPXZrSlFqeGtLM1phTVRGT0w3ME54ZklzdDY2TmhBb0dBSFdJ"
    "MFxuU093Q0FzQUc2NFFQYTJuMmJWRXg3TGgybFRnaERhQnF0bFQwcUk0NkpoSzdQV1g4T1NlUGlG"
    "c21YRzl0TmQ5VFxuNkN5YUd0TTBkVkxWZkQwSmFBcEtXMXpRM1h1SXMwdXBaL3E5Y1NtbVRGcjhp"
    "Qy9Zd3dMM1lWTTFMVnZOajNQVlxuQnBNOUw5NFh2UUJxbnpCbmVhdmFJV2hwcEZEaDlhczhzSkox"
    "WDBDZ1lFQXpCMElpRW9mQWNNcmFTNkFCcnJJXG5jTGFZcms5WHJEOFdhYkpKVGRhdWtIb2dPU0Nx"
    "NjdJcHlSZmRVVlBxNmVYL0FyTWUwR3JFYml2NjdnakwvZWprXG43M1doQ3BXS0MrWjVvSGlBcVh0"
    "Z24wSW1PcnV4QUpWRk43NzYwVXNSc0d2UUdDZkZOTEorcm1NYnY5emtYMGkxXG5GaU54cm1WQmRn"
    "eDJsVlpxR2hyUUprPSIsCiAgICAtLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4="
)

# Декодируем Base64 строку обратно в PEM-формат для Google API
DECODED_KEY = base64.b64decode(B64_KEY).decode("utf-8").replace("\\n", "\n")

# Авторизационные данные вашего сервисного аккаунта проекта skrp-507012
GOOGLE_CREDS = {
    "type": "service_account",
    "project_id": "skrp-507012",
    "private_key_id": "c190eb31396cca4f23c87e6f975256eb3fa4432a",
    "private_key": DECODED_KEY,
    "client_email": "vnyk-468@://gserviceaccount.com",
    "client_id": "111272482503409086216",
    "auth_uri": "https://google.com",
    "token_uri": "https://googleapis.com",
    "auth_provider_x509_cert_url": "https://googleapis.com",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vnyk-468%40://gserviceaccount.com",
    "universe_domain": "googleapis.com",
}

scope = [
    "https://googleapis.com",
    "https://googleapis.com",
]


def get_gspread_client():
    creds = Credentials.from_service_account_info(GOOGLE_CREDS, scopes=scope)
    return gspread.authorize(creds)


st.set_page_config(
    page_title="Система управления лицензиями", page_icon="🔑", layout="centered"
)

tab1, tab2 = st.tabs(["🆕 Внести данные", "🔍 Поиск по ID"])

# --- ВКЛАДКА 1: ЗАПИСЬ ДАННЫХ В ТАБЛИЦУ ---
with tab1:
    st.header("Внесение новой лицензии")

    with st.form("license_form", clear_on_submit=True):
        user_name = st.text_input("Имя человека").strip()
        user_id = st.text_input("ID человека").strip()
        mine_name = st.text_input("На какую шахту выдана лицензия").strip()
        license_type = st.selectbox("Тип лицензии", ["Добыча", "Продажа"])
        license_expiry = st.date_input(
            "Дата окончания лицензии", min_value=datetime.date.today()
        )
        submit_button = st.form_submit_button(label="Записать в таблицу")

    if submit_button:
        if not user_name or not user_id or not mine_name:
            st.error("Ошибка! Все текстовые поля должны быть заполнены.")
        else:
            formatted_date = license_expiry.strftime("%d.%m.%Y")
            row_to_insert = [
                user_name,
                user_id,
                mine_name,
                license_type,
                formatted_date,
            ]

            try:
                client = get_gspread_client()
                spreadsheet = client.open_by_key(SPREADSHEET_ID)
                sheet = spreadsheet.worksheet("Лист1")

                # Запись новой строки
                sheet.append_row(row_to_insert)

                st.success("Данные успешно внесены в Google Таблицу!")
                st.info(
                    f"Лицензия ({license_type}) для {mine_name} активна до {formatted_date}"
                )
            except Exception as e:
                st.error(f"Не удалось сохранить данные. Ошибка: {e}")


# --- ВКЛАДКА 2: ПОИСК ПО ID ---
with tab2:
    st.header("Проверка сотрудника")
    search_id = st.text_input("Введите ID человека для поиска").strip()
    search_button = st.button("Найти все записи")

    if search_button and search_id:
        try:
            client = get_gspread_client()
            spreadsheet = client.open_by_key(SPREADSHEET_ID)
            sheet = spreadsheet.worksheet("Лист1")
            all_rows = sheet.get_all_values()[1:]

            user_history = []
            for row in all_rows:
                while len(row) < 5:
                    row.append("")

                if len(row) > 1 and str(row[1]).strip() == str(search_id):
                    user_history.append(
                        {
                            "Имя": row[0],
                            "ID": row[1],
                            "Шахта": row[2],
                            "Тип": row[3],
                            "Дата": row[4],
                        }
                    )

            if not user_history:
                st.warning(f"Записей для ID '{search_id}' не найдено.")
            else:
                st.markdown(f"### Найдено записей: {len(user_history)}")
                for idx, record in enumerate(user_history, 1):
                    st.markdown(f"---")
                    st.markdown(f"### 📋 Запись №{idx} ({record['Тип']})")
                    st.write(f"**ФИО:** {record['Имя']}")
                    st.write(f"**ID пользователя:** {record['ID']}")
                    st.write(f"**Название шахты:** {record['Шахта']}")
                    st.write(f"**Действует до:** {record['Дата']}")

        except Exception as e:
            st.error(f"Ошибка при чтении таблицы: {e}")
