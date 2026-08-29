import datetime
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# Точный ID вашей таблицы
SPREADSHEET_ID = "https://docs.google.com/spreadsheets/d/13H-fmBuw2vpzsB5ci6oPzl26-_nZ7LRkhZVpJIG81Uo/edit?usp=sharing"

# Формируем сырой приватный ключ одной текстовой строкой
RAW_KEY = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDHRDMSz5TWhTf2\n"
    "msEpSBgvj3hRE1eqLBMYg7sceUb5FjV5hYn1NS7dsYwXlqgMYGbAIWvzK9TZAeQD\n"
    "O+HxikwArNKG43LUwZ1KNQlCIybpLKY4bmvwSuAzZFO7igIvu4+E8HXzVsOwIaLa\n"
    "EANxwdVaH8Xftr66reIgXeUmFdcl2Y6xt/aj2NJKeGekH0WtNyle1QYJbk1eCgSR\n"
    "8FjnCfyk/1+HIpjpa3sf74+uvOpY5p9m13qaQffU7lne/NInFfi7rL+2T5z5LUps\n"
    "y0pPJpC8QakPkBFk+NwtxpzddmzvIj5aGAuZweeO1wDI5TbneVObzN3MetFMrFqN\n"
    "vJx9xjp9AgMBAAECggEAF0/6Bq8c610CD1qLEyyRUc0f5yJTbQADiuhsdVgV7tHD\n"
    "l1BBc9vRPBQHvwG77ti/ZKZ0VepwmCPRvHQeyq6iliih57CH8G6nW3VpfCCXLovv\n"
    "9WWrwJzN7o1EA4qRl2qCz6t/LSUfN0W0Iv1hHceu0YCqmnHrjfUGYcGCa8p91XpR\n"
    "xL4avE9Xs+npkaOVXNprrGLw2OA3r3n63U3gAyQqyC6MgVG8yoBv2470Z+upcnzU\n"
    "23CsbaTqKY+12JXpLS4wB79p80iZ11S2ngXr3lYZbw7YRoPi3NGBoubS5qTyXbn5\n"
    "KiEXNSwfpbt7winbDxojmwS2kdfxbkKncZwum0JzqQKBgQDrGVUZTvGhkSLyQRol\n"
    "UbVpT3zThx77JahBvnmVBFh6WJnQHfbJshj2yL4Thg0ZBbBnKDvjJ6e+izlAufSB\n"
    "BY8OFuLUd6lk454spXKYG202cxhOmPQNBpCTn9HWjfFn7hkGVGrcMyEtmqXvTXdq\n"
    "EeXl7uDcRcecZ8CdnGD7N9+w6QKBgQDY+1isYvcqmvI6S5nfj3EjcI95Eu5d0x/7\n"
    "bVyHGcmGwshASs3mXPxP1kCNiJoi1rZlYIm/68JBSQs8aPYx2/25NJiUlgA9R0gM\n"
    "0VHwQTsZykZh0mXqJtpTAh3zGChj8pNgeB/qFduSXjJWXdna/hYnuqaWeLfSYdm1\n"
    "rAN8GLtgdQKBgAmDcOohQ63iDaP39nLkJ48nZEm7AgnvsCtY5dqd3ma1ByRg0ge/\naTszTF3F4unMTSMfgazjgeo4AA0aeUZvTyamzm8CmJw4icIMv+Jf2b+GUMl9bwLH\n"
    "7TnMEdW40Lf/7otPBzP57bHGvEg+vkJQjxkK3ZaMTFOL70NxfIst66NhAoGAHWI0\n"
    "SOwCAsAG64QPa2n2bVEx7Lh2lTghDaBqtlT0qI46JhK7PWX8OSePiFsmXG9tNd9T\n"
    "6CyaGtM0dVLVfD0JaApKW1zQ3XuIs0upZ/q9cSmmTFr8uC/YwwL3YVM1LQvNj3PV\n"
    "BpM9L94XvQBqnzBneavaIWhppFDh9as8sZJ71X0CgYEAzB0IiEofAcMraS6ABrrI\ncLaYrk9XrD8WabvJTdaukHogOSCq67IpyRfdVUFq6eX/ArMe0GrEbiv67gjL/ejk\n"
    "73WhCpWKC+Z5oHiAqXtgn0ImOruxAJVFN7760UsRsGvQGCfNFNJ+rmMbv9zkX0i1\n"
    "FiNxrmVQdgx2lkVZqGhrQJk=\n"
    "-----END PRIVATE KEY-----\n"
)

# Новые авторизационные данные вашего личного проекта skrp-507012
GOOGLE_CREDS = {
    "type": "service_account",
    "project_id": "skrp-507012",
    "private_key_id": "c190eb31396cca4f23c87e6f975256eb3fa4432a",
    "private_key": RAW_KEY,
    "client_email": "vnyk-468@skrp-507012.iam.gserviceaccount.com",
    "client_id": "111272482503409086216",
    "auth_uri": "https://google.com",
    "token_uri": "https://googleapis.com",
    "auth_provider_x509_cert_url": "https://googleapis.com",
    "client_x509_cert_url": "https://googleapis.com",
    "universe_domain": "googleapis.com",
}

scope = [
    "https://googleapis.com",
    "https://googleapis.com",
]


# Функция подключения к Google API
def get_gspread_client():
    fixed_creds = GOOGLE_CREDS.copy()
    # Заменяем системные символы для корректного чтения ключа шифрования
    fixed_creds["private_key"] = fixed_creds["private_key"].replace("\\n", "\n")

    creds = Credentials.from_service_account_info(fixed_creds, scopes=scope)
    return gspread.authorize(creds)


st.set_page_config(
    page_title="Система управления лицензиями", page_icon="🔑", layout="centered"
)

tab1, tab2 = st.tabs(["🆕 Внести данные", "🔍 Поиск по ID"])

# --- ВКЛАДКА 1: ДОБАВЛЕНИЕ СТРОКИ ---
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
                sheet = client.open_by_key(SPREADSHEET_ID).sheet1

                # Запись новой лицензии в таблицу
                sheet.append_row(row_to_insert)

                st.success("Данные успешно внесены в Google Таблицу!")
                st.info(
                    f"Лицензия ({license_type}) для {mine_name} активна до {formatted_date}"
                )
            except Exception as e:
                st.error(f"Не удалось сохранить данные. Ошибка: {e}")


# --- ВКЛАДКА 2: ВЕРТИКАЛЬНЫЙ ВЫВОД ИСТОРИИ ПО ID СЛУЖАЩЕГО ---
with tab2:
    st.header("Проверка сотрудника")
    search_id = st.text_input("Введите ID человека для поиска").strip()
    search_button = st.button("Найти все записи")

    if search_button and search_id:
        try:
            client = get_gspread_client()
            sheet = client.open_by_key(SPREADSHEET_ID).sheet1
            all_rows = sheet.get_all_values()[1:]  # Убираем заголовки таблицы

            user_history = []
            for row in all_rows:
                while len(row) < 5:
                    row.append("")  # Добиваем пустые ячейки до 5 полей

                # Сверяем ID строго по второму столбцу таблицы (столбец B, индекс 1)
                if len(row) > 1 and row[1].strip() == search_id:
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
                st.write("Все лицензии человека отображены ниже в столбец:")

                # Выводим карточки последовательно в столбец одна за другой
                for idx, record in enumerate(user_history, 1):
                    st.markdown(f"---")
                    st.markdown(f"### 📋 Запись №{idx} ({record['Тип']})")
                    st.write(f"**ФИО:** {record['Имя']}")
                    st.write(f"**ID пользователя:** {record['ID']}")
                    st.write(f"**Название шахты:** {record['Шахта']}")
                    st.write(f"**Действует до:** {record['Дата']}")

        except Exception as e:
            st.error(f"Ошибка при чтении таблицы: {e}")
