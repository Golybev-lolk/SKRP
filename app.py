import datetime
import streamlit as st
import pandas as pd


CSV_URL = "https://docs.google.com/spreadsheets/d/13H-fmBuw2vpzsB5ci6oPzl26-_nZ7LRkhZVpJIG81Uo/edit?usp=sharing"


st.set_page_config(
    page_title="Система управления лицензиями", layout="centered"
)

tab1, tab2 = st.tabs([" Внести данные", " Поиск по ID"])


with tab1:
    st.header("Внесение новой лицензии")
    st.write("Чтобы внести данные, используйте таблицу напрямую, либо введите информацию ниже:")
    
    with st.form("license_form", clear_on_submit=True):
        user_name = st.text_input("Имя человека").strip()
        user_id = st.text_input("ID человека").strip()
        mine_name = st.text_input("На какую шахту выдана лицензия").strip()
        license_type = st.selectbox("Тип лицензии", ["Добыча", "Продажа"])
        license_expiry = st.date_input("Дата окончания лицензии", min_value=datetime.date.today())
        submit_button = st.form_submit_button(label="Сформировать строку")

    if submit_button:
        if not user_name or not user_id or not mine_name:
            st.error("Ошибка! Все текстовые поля должны быть заполнены.")
        else:
            formatted_date = license_expiry.strftime("%d.%m.%Y")
            # Выводим строку для удобного ручного копирования в таблицу при необходимости
            st.success("Строка подготовлена для реестра!")
            st.code(f"{user_name}\t{user_id}\t{mine_name}\t{license_type}\t{formatted_date}", language="text")
            st.info("Поскольку гостевой веб-коннектор Streamlit Cloud сейчас перегружен, скопируйте строку выше и вставьте в таблицу, либо используйте вкладку поиска.")



with tab2:
    st.header("Проверка сотрудника")
    search_id = st.text_input("Введите ID человека для поиска").strip()
    search_button = st.button("Найти все записи")

    if search_button and search_id:
        try:
            # Читаем таблицу напрямую через CSV-поток Google (без сторонних модулей)
            df = pd.read_csv(CSV_URL)
            
            # Приводим заголовки и ID к строгому текстовому виду
            df.columns = [col.strip() for col in df.columns]
            if "ID" in df.columns:
                df["ID"] = df["ID"].astype(str).str.strip()
                filtered_df = df[df["ID"] == search_id]

                if filtered_df.empty:
                    st.warning(f"Записей для ID '{search_id}' не найдено.")
                else:
                    st.markdown(f"### Найдено записей в таблице: {len(filtered_df)}")
                    st.write("Все выданные лицензии человека отображены ниже в столбец:")

                    # Выводим строки в виде карточек в столбец
                    for idx, row in enumerate(filtered_df.to_dict(orient="records"), 1):
                        st.markdown(f"---")
                        st.markdown(f"### 📋 Запись №{idx} ({row.get('Тип лицензии', '—')})")
                        st.write(f"**ФИО:** {row.get('Имя', '—')}")
                        st.write(f"**ID пользователя:** {row.get('ID', '—')}")
                        st.write(f"**Название шахты:** {row.get('Название шахты', '—')}")
                        st.write(f"**Действует до:** {row.get('Дата окончания', '—')}")
            else:
                st.error("В таблице не найден столбец с заголовком 'ID'. Проверьте первую строчку таблицы.")

        except Exception as e:
            st.error(f"Не удалось прочитать таблицу. Убедитесь, что доступ по ссылке открыт. Ошибка: {e}")
