import datetime
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Указываем прямую ссылку на вашу Google Таблицу
TABLE_URL = "https://docs.google.com/spreadsheets/d/13H-fmBuw2vpzsB5ci6oPzl26-_nZ7LRkhZVpJIG81Uo/edit?usp=sharing"

st.set_page_config(
    page_title="Система управления лицензиями", layout="centered"
)

tab1, tab2 = st.tabs([" Внести данные", " Поиск по ID"])

# --- ВКЛАДКА 1: ФОРМА ВВОДА ДАННЫХ ---
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
                # Подключаемся через встроенный коннектор Streamlit
                conn = st.connection("gsheets", type=GSheetsConnection)

                # Скачиваем текущие данные, чтобы дописать строку вниз
                df = conn.read(spreadsheet=TABLE_URL, ttl=0)

                # Создаем новую строку
                new_row = {
                    "Имя": user_name,
                    "ID": user_id,
                    "Название шахты": mine_name,
                    "Тип лицензии": license_type,
                    "Дата окончания": formatted_date,
                }

                # Добавляем строку и отправляем обновленную таблицу назад в Google
                df = df.append(new_row, ignore_index=True)
                conn.update(spreadsheet=TABLE_URL, data=df)

                st.success("Данные успешно внесены в таблицу!")
                st.info(
                    f"Лицензия ({license_type}) для {mine_name} активна до {formatted_date}"
                )
            except Exception as e:
                st.error(f"Не удалось сохранить данные. Ошибка: {e}")

# --- ВКЛАДКА 2: ВЫВОД ИСТОРИИ ПО ID ---
with tab2:
    st.header("Проверка сотрудника")
    search_id = st.text_input("Введите ID человека для поиска").strip()
    search_button = st.button("Найти все записи")

    if search_button and search_id:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read(spreadsheet=TABLE_URL, ttl=0)

            # Фильтруем данные из датафрейма по столбцу 'ID'
            # Приводим типы к строкам, чтобы избежать ошибок сравнения чисел
            df["ID"] = df["ID"].astype(str).str.strip()
            filtered_df = df[df["ID"] == search_id]

            if filtered_df.empty:
                st.warning(f"Записей для ID '{search_id}' не найдено.")
            else:
                st.markdown(f"### Найдено записей: {len(filtered_df)}")
                st.write("Все лицензии человека отображены ниже в столбец:")

                # Перебираем найденные строки и выводим карточками в столбец
                for idx, row in enumerate(filtered_df.to_dict(orient="records"), 1):
                    st.markdown(f"---")
                    st.markdown(f"### Запись №{idx} ({row.get('Тип лицензии', '—')})")
                    st.write(f"**ФИО:** {row.get('Имя', '—')}")
                    st.write(f"**ID пользователя:** {row.get('ID', '—')}")
                    st.write(f"**Название шахты:** {row.get('Название шахты', '—')}")
                    st.write(f"**Действует до:** {row.get('Дата окончания', '—')}")

        except Exception as e:
            st.error(f"Ошибка при чтении таблицы: {e}")
