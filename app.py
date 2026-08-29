import datetime
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

scope = [
    "https://googleapis.com",
    "https://googleapis.com",
]

def get_gspread_client():
    if "gcp_service_account" in st.secrets:
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    else:
        creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    return gspread.authorize(creds)

st.set_page_config(
    page_title="Система управления лицензиями", layout="centered"
)

tab1, tab2 = st.tabs(["Внести данные", "Поиск по ID"])

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
                sheet = client.open("Лицензии").sheet1
                sheet.append_row(row_to_insert)
                st.success("Данные успешно внесены в таблицу!")
                st.info(
                    f"Лицензия ({license_type}) для {mine_name} активна до {formatted_date}"
                )
            except Exception as e:
                st.error(f"Не удалось сохранить данные. Ошибка: {e}")

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

                if row[1].strip() == search_id:  # Проверка строго по столбцу ID (индекс 1)
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
                    st.markdown(f"### Запись №{idx} ({record['Тип']})")
                    st.write(f"**ФИО:** {record['Имя']}")
                    st.write(f"**ID пользователя:** {record['ID']}")
                    st.write(f"**Название шахты:** {record['Шахта']}")
                    st.write(f"**Действует до:** {record['Дата']}")

        except Exception as e:
            st.error(f"Ошибка при чтении таблицы: {e}")
