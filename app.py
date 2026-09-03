import datetime
import streamlit as st
import requests

API_URL = "https://script.google.com/macros/s/AKfycbzsjU2Y0CNstQftN58fJPLOuCyZxlPcYRdhCPAIenXhHGWKc7zwkr8DNTqhawiY3F2c/exec"

st.set_page_config(
    page_title="Система управления лицензиями", layout="centered"
)
tab1, tab2 = st.tabs(["Ну тут типа писать буквы", "Поиск читоса по ID"])
with tab1:
    st.header("Внесение новой лицензии")
    with st.form("license_form", clear_on_submit=True):
        user_name = st.text_input("Имя существа").strip()
        user_id = st.text_input("ID существа").strip()
        mine_name = st.text_input("На что выдана лицензия?").strip()
        license_type = st.selectbox("Тип лицензии", ["Добыча", "Продажа"])
        license_expiry = st.date_input(
            "Дата окончания лицензии", min_value=datetime.date.today()
        )
        submit_button = st.form_submit_button(label="Записать в таблицу")
    if submit_button:
        if not user_name or not user_id or not mine_name:
            st.error("Ошибка! Все текстовые поля должны иметь символы. Меняй!.")
        else:
            payload = {
                "name": user_name,
                "id": user_id,
                "mine": mine_name,
                "type": license_type,
                "expiry": license_expiry.isoformat()
            }
            try:
                response = requests.post(API_URL, json=payload).json()
                if response.get("status") == "success":
                    st.success("Данные успешно внесены в Таблицу! Молодец епта!")
                    st.info(f"Лицензия активна. Срок: {datetime.date.today().strftime('%d.%m.%Y')} - {license_expiry.strftime('%d.%m.%Y')}")
                else:
                    st.error(f"Ошибка скрипта таблицы 0_0: {response.get('message')}")
            except Exception as e:
                st.error(f"Не удалось связаться с таблицей. ХУЙ: {e}")

with tab2:
    st.header("Поиск записей про чела по ID")
    search_id = st.text_input("Введите ID читоса для поиска").strip()
    search_button = st.button("ИСКАТЬ!")

    if search_button and search_id:
        try:
            response = requests.get(f"{API_URL}?id={search_id}").json()

            if not response:
                st.warning(f"Записей для ID '{search_id}' не найдено.")
            else:
                st.markdown(f"### Найдено записей: {len(response)}")
                st.write("Все лицензии существа отображены ниже от старых к новым:")

                for idx, record in enumerate(response, 1):
                    st.markdown(f"---")
                    st.markdown(f"### Запись №{idx} ({record['type']})")
                    st.write(f"**ФИО:** {record['name']}")
                    st.write(f"**ID пользователя:** {record['id']}")
                    st.write(f"**Название шахты:** {record['mine']}")
                    
                    st.write(f"**Срок действия лицензии:** {record.get('today', '—')} - {record.get('expiry', '—')}")

        except Exception as e:
            st.error(f"Ошибка при чтении данных из таблицы. БЛЯТЬ: {e}")
