import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

st.image("https://teatrium.ru/upload/medialibrary/af0/2t0u03cf8i13p4o0oven20z5gasagnjl/vtb.jpg",
         use_column_width=True)
st.title('Внутригрупповый конкурс по продажам')
st.header('Первая группа')

if 'sign in' not in st.session_state:
    st.session_state['sign in'] = False

text_input_container_4 = st.sidebar.empty()
button_logout = None

if st.session_state["sign in"] == False:
    st.sidebar.error("Для работы этой вкладки выполните вход в систему на вкладке 'competition feb'")
else:
    button_logout = text_input_container_4.button("Выйти")
    if button_logout:
        st.session_state["sign in"] = False
    st.sidebar.info(f'Вход выполнен пользователем - {st.session_state["user"]}')

    url = 'https://docs.google.com/spreadsheets/d/1MpYAg1WwQMHliB5bCZ8FNabZz25eEWBUsQKYRTYLZ0A/export?format=csv&gid=1672766275'
    # Прочитайте данные в DataFrame
    df = pd.read_csv(url)
    df.set_index("ФИО", inplace=True)
    df = df.head(10)

    df['Баллы'] = df['Баллы'].str.replace(',', '.', regex=False)
    df['Баллы'] = pd.to_numeric(df['Баллы'], errors='coerce')

    fig = px.pie(
        names=df.index.to_list(), 
        values=df['Баллы'].to_list(), 
        title="Баллы")

    st.plotly_chart(fig)

    url_t = 'https://docs.google.com/spreadsheets/d/1MpYAg1WwQMHliB5bCZ8FNabZz25eEWBUsQKYRTYLZ0A/export?format=csv&gid=628014439'
    df_t=pd.read_csv(url_t)
    df_t.set_index("Дата", inplace=True)
    df_t['Баллы'] = df_t['Баллы'].str.replace(',', '.', regex=False)

    today = datetime.today().date()
    yesterday = datetime.today() - timedelta(days=1)

    yesterday_str = yesterday.strftime("%Y-%m-%d")

    other_date = datetime(2025, 2, 28).date()
    if today <= other_date:
        dft_s = df_t[:f'{yesterday_str}']
    else:
        dft_s = df_t

    # Создание фигуры
    fig = go.Figure()

    # Добавление первого графика (Продажи)
    fig.add_trace(go.Scatter(
        x=dft_s.index.to_list(), 
        y=dft_s['Баллы'],
        mode='lines', 
        name='Баллы',
        line=dict(color='blue')
    ))

    # Настройка макета
    fig.update_layout(
        title='Темп роста общего коэффициента продаж',
        xaxis_title='Дата',
        yaxis_title='Баллы',
        hovermode='x unified'
    )

    # Отображение графика в Streamlit
    st.plotly_chart(fig, use_container_width=True)

    sel_param = st.selectbox(
        "Выберите показатель",
        ("ПДС", "СОМ", "Допка", "Пакет",
        "Автостяг", "Пенсия", "НС", "АПЖКУ",
        "Сим-карта", "Кросс КК"),
    )

    button_par = st.button("Выбрать")

    if button_par:
        st.subheader(f'{sel_param}')

        df = df.sort_values(by=f'{sel_param}', ascending=False)

        # Создание столбчатой диаграммы
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df.index.to_list(),
            y=df[f'{sel_param}'],
            marker_color='skyblue'  # Цвет столбцов
        ))

        # Настройка макета
        fig.update_layout(
            title='Рейтинг МКМ по данному показателю',
            xaxis_title='МКМ',
            yaxis_title=f'{sel_param}'
        )
        st.plotly_chart(fig, use_container_width=True)  

        # Создание линейной диаграммы
        fig = go.Figure()

        # Добавление графика (Продажи)
        fig.add_trace(go.Scatter(
            x=dft_s.index.to_list(), 
            y=dft_s[f'{sel_param}'],
            mode='lines', 
            name=f'{sel_param}',
            line=dict(color='blue')
        ))

        # Настройка макета
        fig.update_layout(
            title=f'Темп роста показателя "{sel_param}" по дате',
            xaxis_title='Дата',
            yaxis_title=f'{sel_param}',
            hovermode='x unified'
        )

        # Отображение графика в Streamlit
        st.plotly_chart(fig, use_container_width=True)