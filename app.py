import datetime
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# Данные авторизации вшиты напрямую из вашего JSON-файла
GOOGLE_CREDS = {
    "type": "service_account",
    "project_id": "gen-lang-client-0637058958",
    "private_key_id": "ec7efaf300e156f779dba1f54c13cd778dc91bb8",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC8h+V7e+N25MQp\nDL4n/TsdUiNyAL4rDyIuEBX0huXbRRLfSX2svuPoL9I8iyNlnk/c2VebhKrav/jL\nZnvcDbBbZObRdCT3OZei5mLBNBYC/NWBRCvSMWltN9caMyH/ZdokUhJ41QxVMR1J\nvscJ02Yei+4MmuikXNXajt+LsTnoHXkQvT2DMbPbFj2s9GqoskE7ELgxHuzwFoOC\n5EH0grIphSi5D5RHA5oGU4oUrhRbqvbB9aydPMKRhODvGZFnC7ZCBPBMfFA5m/74\niGkG7XkML4z97YkfdK9pCY+4zVfXk9jI+iHFVb2wQn936Mg6GYYRRu8EX+VD3IEw\ncJ74R2JdAgMBAAECggEARy7GUhPqQ+NHPzqM95tQvRbcxDgMlURvAtZW+88NLXeM\nkxrz5QvkEDAyIGLmeAFIpRm4zsLOIa7W+LFWtbTDcBaOYeoI5QFtQ/fZtJn+b51X\n3alIJGI8rJynTkCdJwmlTg5g5BeIwwe6x7PNAeQ8C++Ib2Dz0s8sfYtxUxSUyRLl\nE95DypgkwVs4x6v8nloYcExPne35MGFPOpO5W84hfY795Ivy4huitstVp7vzaT2n\nl/Kqzran3jqalQnV4NtKzCE4yuwpwp4ZN2q5NZAoGls7IMUa8gj7fpvRbrm7GWkU\nO8ifi/m2bazd0ZhZr0B0veotHsimORMQ7J8x64G4nwKBgQDxl88ZwnazAPjd443B\nZ92RBSN/2Ty+ySFDTnVPCRrwkDlUCLZw4ffnschQ5cFotUXlZsITZuQIyHJoQwz5\nRfHvV8Z9doAXR6heurIwVz1Mf+TDLmNRylIOUaPdCYBYXzyd/Y5GLqqrMRVmZJUR\nA/K6NvXE0gR7ugzCuTxwUYiFkwKBgQDHxgiPnnIFWjdB/fr+ycu3L02DjeXM0Nxf\nlFVqkqTpeCS8G2RX6guJv/U57W9V6wcYEyK6JNzYVmvIal7CzFy5ADUt+nWnUiMt\nOQLaA8JNnjZxj8QyUuLFGUmL/HEpywL7nVkbngV5aYEEdkbrl0adWvD0TmLUgCPy\nrGZ+O9tuTwKBgFsfhlbR+VF1CWkv3hTX50M+q/AZ8QaI+EnZuvdvmMCptWXTz3Ru\VsIGVWbl8fhbfxySkJse0N3bNQPMXoVa83DyK4TBAHlHZuMsCe+fyBglmRRhV8bO\nx/psoqDJZ6ZtbYCt1U71ZRwi7E5tm6gKVDAWcMam7Ff6ibucgIZgylyPAoGBALZC\n5uyhEkXv2RpMLgLm+QVYEtBDVbVXmLdbDdL9l5eqFVnJY/MRhRVYHNOM3Fb25rIA\nQ16w4ww9THi9E1eGO9JNbjdUmqLdPVq0+PUPGObXwbQ6BjYjiOFqAL/GwTfwD/if\nxfx8X2I174+ymWG30qUdo1hBa8mUXze4MopY8gnhAoGBANxHUWvTOH28ot5pO+qy\nuuLMzB6KlJfrgFnXk3miWojy4iixC2nqPVmy3KAE2oxWpcCor6dkNG8t8IYu9SSz\neX1mIeW6lomEFIGpAouY8l9/q3sa6V8028RQ9asNsRHiEUL7U6683U3ruyGi8hGt\na/Hwa5FpRaB4ZycgWiYWW5kP\n-----END PRIVATE KEY-----\n",
    "client_email": "skyrimik@://gserviceaccount.com",
    "client_id": "101670696874417843186",
    "auth_uri": "https://google.com",
    "token_uri": "https://googleapis.com",
    "auth_provider_x509_cert_url": "https://googleapis.com",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/skyrimik%40://gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

scope = [
    "https://googleapis.com",
    "https://googleapis.com"
]

def get_gspread_client():
    # Подключение выполняется напрямую по вшитому словарю
    creds = Credentials.from_service_account_info(GOOGLE_CREDS, scopes=scope)
    return gspread.authorize(creds)

st.set_page_config(page_title="Система управления лицензиями", layout="centered")

tab1, tab2 = st.tabs([" Внести данные", " Поиск по ID"])

# --- ВКЛАДКА 1: ФОРМА ВВОДА ДАННЫХ ---
with tab1:
    st.header("Внесение новой лицензии")
    with st.form("license_form", clear_on_submit=True):
        user_name = st.text_input("Имя человека").strip()
        user_id = st.text_input("ID человека").strip()
        mine_name = st.text_input("На какую шахту выдана лицензия").strip()
        license_type = st.selectbox("Тип лицензии", ["Добыча", "Продажа"])
        license_expiry = st.date_input("Дата окончания лицензии", min_value=datetime.date.today())
        submit_button = st.form_submit_button(label="Записать в таблицу")

    if submit_button:
        if not user_name or not user_id or not mine_name:
            st.error("Ошибка! Все текстовые поля должны быть заполнены.")
        else:
            formatted_date = license_expiry.strftime("%d.%m.%Y")
            row_to_insert = [user_name, user_id, mine_name, license_type, formatted_date]

            try:
                client = get_gspread_client()
                sheet = client.open("Лицензии").sheet1
                sheet.append_row(row_to_insert)
                st.success("Данные успешно внесены в таблицу!")
                st.info(f"Лицензия ({license_type}) для {mine_name} активна до {formatted_date}")
            except Exception as e:
                st.error(f"Не удалось сохранить данные. Ошибка: {e}")

# --- ВКЛАДКА 2: ВЫВОД ИСТОРИИ В СТОЛБЕЦ ПО ID ---
with tab2:
    st.header("Проверка сотрудника")
    search_id = st.text_input("Введите ID человека для поиска").strip()
    search_button = st.button("Найти все записи")

    if search_button and search_id:
        try:
            client = get_gspread_client()
            sheet = client.open("ЛИЦЕНЗИИ").sheet1
            all_rows = sheet.get_all_values()[1:]

            user_history = []
            for row in all_rows:
                while len(row) < 5:
                    row.append("")

                # Проверяем совпадение по второму столбцу (индекс 1)
                if len(row) > 1 and row[1].strip() == search_id:
                    user_history.append({
                        "Имя": row[0],
                        "ID": row[1],
                        "Шахта": row[2],
                        "Тип": row[3],
                        "Дата": row[4]
                    })

            if not user_history:
                st.warning(f"Записей для ID '{search_id}' не найдено.")
            else:
                st.markdown(f"### Найдено записей: {len(user_history)}")
                for idx, record in enumerate(user_history, 1):
                    st.markdown(f"---")
                    st.markdown(f"### Запись №{idx} ({record['Тип']})")
                    st.write(f"**ФИО:** {record['Имя']}")
                    st.write(f"**ID пользователя:** {record['ID']}")
                    st.write(f"**Название шахты:** {record['Шахта']}")
                    st.write(f"**Действует до:** {record['Дата']}")

        except Exception as e:
            st.error(f"Ошибка при чтении таблицы: {e}")
