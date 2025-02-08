import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

st.image("https://teatrium.ru/upload/medialibrary/af0/2t0u03cf8i13p4o0oven20z5gasagnjl/vtb.jpg",
         use_column_width=True)
st.title('Внутригрупповый конкурс по продажам')

# st.write("Hello world")

# tab = pd.read_excel('C:/Users/ivano/Desktop/Конкурс_групп/Группа.xlsx')
# tab.set_index('ФИО', inplace=True)
# st.dataframe(tab)

df_auth = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRk8UfW-agKMGralUkIeF4zIRUI1JP1Mx7j0ReFrO6IDfrKFL_FrlMZXYMpTFWex5RkwZl_7hSdfVwD/pub?output=csv')

text_input_container_0 = st.sidebar.empty()
text_input_container_1 = st.sidebar.empty()
text_input_container_2 = st.sidebar.empty()
text_input_container_3 = st.sidebar.empty()
text_input_container_4 = st.sidebar.empty()


# st.sidebar.success("Select a page above.")

if "login" not in st.session_state:
    st.session_state["login"] = ""

if "password" not in st.session_state:
    st.session_state["password"] = ""

if "user" not in st.session_state:
    st.session_state["user"] = ""

if "sign in" not in st.session_state:
    st.session_state["sign in"] = False

button_sign_in = None
button_logout = None

if st.session_state["sign in"] == False:
    text_input_container_0.title("Авторизация")
    login = text_input_container_1.text_input("Логин", st.session_state["login"], placeholder="login")
    st.session_state["login"] = login
    password = text_input_container_2.text_input("Пароль", st.session_state["password"], placeholder="password", type='password')
    st.session_state["password"] = password

    button_sign_in = text_input_container_3.button("Войти")
else:
    st.sidebar.info(f'Вход выполнен пользователем - {st.session_state["user"]}')
    #st.write(f'{datetime.now}')
    #st.dataframe(df_auth)

    button_logout = text_input_container_4.button("Выйти")
    if button_logout:
        st.session_state["sign in"] = False

    names_groops = ['/','Группа 1', 'Группа 2']

    # Первая группа
    # Укажите URL таблицы (должен быть опубликован для всех)
    url1 = 'https://docs.google.com/spreadsheets/d/1MpYAg1WwQMHliB5bCZ8FNabZz25eEWBUsQKYRTYLZ0A/export?format=csv&gid=1672766275'
    # Прочитайте данные в DataFrame
    df1 = pd.read_csv(url1)
    df1.set_index("ФИО", inplace=True)
    df_1 = df1.copy()
    # Удалить все строки, кроме строки с индексом 1
    df_1 = df_1.query('index == "Итог"') 
    # Переименуйте индекс
    new_index = pd.Index([names_groops[1]])  # Новый индекс
    df_1 = df_1.set_axis(new_index, axis='index')

    # Укажите URL таблицы (должен быть опубликован для всех)
    url2 = 'https://docs.google.com/spreadsheets/d/1BQOy0f7JDxAwjd-mvKCx-l42ZoASl0IkxCGJwNyfoiI/export?format=csv&gid=1672766275'
    df2 = pd.read_csv(url2)
    df2.set_index("ФИО", inplace=True)
    df_2 = df2.copy()
    # Удалить все строки, кроме строки с индексом 1
    df_2 = df_2.query('index == "Итог"') 
    # Переименуйте индекс
    new_index = pd.Index([names_groops[2]])  # Новый индекс
    df_2 = df_2.set_axis(new_index, axis='index')

    ##Объединение таблиц
    df_0 = pd.concat([df_1, df_2])

    df_0['Баллы'] = df_0['Баллы'].str.replace(',', '.', regex=False)
    df_0['Баллы'] = pd.to_numeric(df_0['Баллы'], errors='coerce')
    labels=df_0.index

    values = df_0['Баллы']

    fig = px.pie(
        names=df_0.index.to_list(), 
        values=df_0['Баллы'].to_list(), 
        title="Баллы")


    st.plotly_chart(fig)


    df_10 = df1.copy()
    df_10 = df_10.query('index != "Итог"')
    df_10['Баллы'] = df_10['Баллы'].str.replace(',', '.', regex=False) 
    df_10 = (df_10
                .sort_values('Баллы',
                                ascending=False)
                .head(1)
            )
    df_10.index = df_10.index + ' (1гр.)'

    df_20 = df2.copy()
    df_20 = df_20.query('index != "Итог"')
    df_20['Баллы'] = df_20['Баллы'].str.replace(',', '.', regex=False) 
    df_20 = (df_20
                .sort_values('Баллы', 
                            ascending=False)
                .head(1)
            )
    df_20.index = df_20.index + ' (2гр.)'
    # st.dataframe(df_20[[sel_param]].head(1))

    df_00 = pd.concat([df_10, df_20])

    # Создание столбчатой диаграммы
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_00.index.to_list(),
        y=df_00['Баллы'],
        marker_color='skyblue'  # Цвет столбцов
    ))

    # Настройка макета
    fig.update_layout(
        title='Топы',
        xaxis_title='Лидеры',
        yaxis_title='Баллы'
    )
    st.plotly_chart(fig, use_container_width=True)

    # показатели
    url1t = 'https://docs.google.com/spreadsheets/d/1MpYAg1WwQMHliB5bCZ8FNabZz25eEWBUsQKYRTYLZ0A/export?format=csv&gid=628014439'
    df1t=pd.read_csv(url1t)
    df1t.set_index("Дата", inplace=True)
    df1t_b = df1t[['Баллы']]
    df1t_b['Баллы'] = df1t_b['Баллы'].str.replace(',', '.', regex=False)
    df1t_b = (df1t_b
        .rename(
            columns={'Баллы': 'Группа 1'}))

    url2t = 'https://docs.google.com/spreadsheets/d/1BQOy0f7JDxAwjd-mvKCx-l42ZoASl0IkxCGJwNyfoiI/export?format=csv&gid=628014439'
    df2t=pd.read_csv(url2t)
    df2t.set_index("Дата", inplace=True)
    df2t_b = df2t[['Баллы']]
    df2t_b['Баллы'] = df2t_b['Баллы'].str.replace(',', '.', regex=False)
    df2t_b = (df2t_b
        .rename(
            columns={'Баллы': 'Группа 2'}))

    # Объединяем таблицы по общему индексу
    df0t_b = df1t_b.join(df2t_b)

    today = datetime.today().date()
    yesterday = datetime.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    # Задаем другую дату для сравнения (например, 2023-10-01)
    other_date = datetime(2025, 2, 28).date()
    if today <= other_date:
        df0t_b_s = df0t_b[:f'{yesterday_str}']
        # st.write("today <= other_date")
        # st.dataframe(df0t_b)
    else:
        df0t_b_s = df0t_b



    # Создание фигуры
    fig = go.Figure()

    # Добавление первого графика (Продажи)
    fig.add_trace(go.Scatter(
        x=df0t_b_s.index.to_list(), y=df0t_b_s['Группа 1'],
        mode='lines', name='Группа 1',
        line=dict(color='blue')
    ))

    # Добавление второго графика (Прибыль)
    fig.add_trace(go.Scatter(
        x=df0t_b_s.index.to_list(), y=df0t_b_s['Группа 2'],
        mode='lines', name='Группа 2',
        line=dict(color='red')
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
        st.header(f'{sel_param}')
        # st.bar_chart(df_0[sel_param])

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_0.index.to_list(),
            y=df_0[f'{sel_param}'],
            marker_color='skyblue'  # Цвет столбцов
        ))

        # Настройка макета
        fig.update_layout(
            title='Общий показатель',
            xaxis_title='Группы',
            yaxis_title=f'{sel_param}'
        )
        st.plotly_chart(fig, use_container_width=True)    

        # st.subheader('Лидеры групп')
        df_10 = df1.copy()
        df_10 = df_10.query('index != "Итог"') 
        df_10 = (df_10
                .sort_values(sel_param,
                                ascending=False)
                .head(1)
                )
        df_10.index = df_10.index + ' (1гр.)'
        # st.dataframe(df_10[[sel_param]].head(1))

        df_20 = df2.copy()
        df_20 = df_20.query('index != "Итог"') 
        df_20 = (df_20
                .sort_values(sel_param, 
                                ascending=False)
                .head(1)
                )
        df_20.index = df_20.index + ' (2гр.)'
        # st.dataframe(df_20[[sel_param]].head(1))

        df_00 = pd.concat([df_10, df_20])

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_00.index.to_list(),
            y=df_00[f'{sel_param}'],
            marker_color='skyblue'  # Цвет столбцов
        ))

        # Настройка макета
        fig.update_layout(
            title='Топы в данном показателе',
            xaxis_title='Лидеры',
            yaxis_title=f'{sel_param}'
        )
        st.plotly_chart(fig, use_container_width=True)

        # st.bar_chart(df_00[sel_param])

        df1t_p = df1t[[f'{sel_param}']]
        df1t_p = (df1t_p
            .rename(
                columns={f'{sel_param}': 'Группа 1'}))

        df2t_p = df2t[[f'{sel_param}']]
        df2t_p = (df2t_p
            .rename(
                columns={f'{sel_param}': 'Группа 2'}))

        df0t_p = df1t_p.join(df2t_p)

        if today <= other_date:
            df0t_p_s = df0t_p[:f'{yesterday_str}']
        else:
            df0t_p_s = df0t_p

        # Создание фигуры
        fig = go.Figure()

        # Добавление первого графика (Продажи)
        fig.add_trace(go.Scatter(
            x=df0t_p_s.index.to_list(), 
            y=df0t_p_s['Группа 1'],
            mode='lines', 
            name='Группа 1',
            line=dict(color='blue')
        ))

        # Добавление второго графика (Прибыль)
        fig.add_trace(go.Scatter(
            x=df0t_p_s.index.to_list(), 
            y=df0t_p_s['Группа 2'],
            mode='lines', 
            name='Группа 2',
            line=dict(color='red')
        ))

        # Настройка макета
        fig.update_layout(
            title=f'Темп роста показателя "{sel_param}" по дате',
            xaxis_title='Дата',
            yaxis_title=f'{sel_param}',
            hovermode='x unified'
        )
        # fig.update_yaxes(dtick=1)

        # Отображение графика в Streamlit
        st.plotly_chart(fig, use_container_width=True)

if button_sign_in:
    true_pass = 0
    for ind in df_auth.index:
        log = df_auth['login'][ind]
        pas = df_auth['password'][ind]        
        if (login == log) & (password == pas):
            text_input_container_0.empty()            
            text_input_container_1.empty()
            text_input_container_2.empty()
            text_input_container_3.empty()
            user = df_auth['Фамилия_Имя'][ind]
            st.session_state["user"] = user
            st.sidebar.info(f'Вход выполнен пользователем - {user}')
            st.session_state["sign in"] = True
            break;
    if st.session_state["sign in"] == False:
        if (login == None) | (password == None):
            st.sidebar.warning('Введите все поля для входа')
        else: 
            st.sidebar.error('Неверный логин/пароль')
        text_input_container_4.empty()
    else:       
        #st.write(f'{datetime.now}')
        #st.dataframe(df_auth)

        button_logout = text_input_container_4.button("Выйти")
        if button_logout:
            st.session_state["sign in"] = False

        names_groops = ['/','Группа 1', 'Группа 2', 'Группа 3']

        # Первая группа
        # Укажите URL таблицы (должен быть опубликован для всех)
        url1 = 'https://docs.google.com/spreadsheets/d/1MpYAg1WwQMHliB5bCZ8FNabZz25eEWBUsQKYRTYLZ0A/export?format=csv&gid=1672766275'
        # Прочитайте данные в DataFrame
        df1 = pd.read_csv(url1)
        df1.set_index("ФИО", inplace=True)
        df_1 = df1.copy()
        # Удалить все строки, кроме строки с индексом 1
        df_1 = df_1.query('index == "Итог"') 
        # Переименуйте индекс
        new_index = pd.Index([names_groops[1]])  # Новый индекс
        df_1 = df_1.set_axis(new_index, axis='index')

        # st.subheader('Вторая группа')
        # Укажите URL таблицы (должен быть опубликован для всех)
        url2 = 'https://docs.google.com/spreadsheets/d/1BQOy0f7JDxAwjd-mvKCx-l42ZoASl0IkxCGJwNyfoiI/export?format=csv&gid=1672766275'
        df2 = pd.read_csv(url2)
        df2.set_index("ФИО", inplace=True)
        df_2 = df2.copy()
        # Удалить все строки, кроме строки с индексом 1
        df_2 = df_2.query('index == "Итог"') 
        # Переименуйте индекс
        new_index = pd.Index([names_groops[2]])  # Новый индекс
        df_2 = df_2.set_axis(new_index, axis='index')

        ##Объединение таблиц
        df_0 = pd.concat([df_1, df_2])

        # st.dataframe(df_0)

        df_0['Баллы'] = df_0['Баллы'].str.replace(',', '.', regex=False)
        df_0['Баллы'] = pd.to_numeric(df_0['Баллы'], errors='coerce')

        # st.subheader('Баллы')
        #Data Set
        labels=df_0.index

        values = df_0['Баллы']


        #The plot
        # fig = go.Figure(
        #     go.Pie(
        #     labels = labels,
        #     values = values,
        #     hoverinfo = "label+percent",
        #     textinfo = "value"
        # ))

        fig = px.pie(
            names=df_0.index.to_list(), 
            values=df_0['Баллы'].to_list(), 
            title="Баллы")


        #st.header("Pie chart")
        st.plotly_chart(fig)


        df_10 = df1.copy()
        df_10 = df_10.query('index != "Итог"')
        df_10['Баллы'] = df_10['Баллы'].str.replace(',', '.', regex=False) 
        df_10 = (df_10
                    .sort_values('Баллы',
                                    ascending=False)
                    .head(1)
                )
        df_10.index = df_10.index + ' (1гр.)'

        df_20 = df2.copy()
        df_20 = df_20.query('index != "Итог"')
        df_20['Баллы'] = df_20['Баллы'].str.replace(',', '.', regex=False) 
        df_20 = (df_20
                    .sort_values('Баллы', 
                                ascending=False)
                    .head(1)
                )
        df_20.index = df_20.index + ' (2гр.)'
        # st.dataframe(df_20[[sel_param]].head(1))

        df_00 = pd.concat([df_10, df_20])

        # Создание столбчатой диаграммы
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_00.index.to_list(),
            y=df_00['Баллы'],
            marker_color='skyblue'  # Цвет столбцов
        ))

        # Настройка макета
        fig.update_layout(
            title='Топы',
            xaxis_title='Лидеры',
            yaxis_title='Баллы'
        )
        st.plotly_chart(fig, use_container_width=True)

        # params = 
        url1t = 'https://docs.google.com/spreadsheets/d/1MpYAg1WwQMHliB5bCZ8FNabZz25eEWBUsQKYRTYLZ0A/export?format=csv&gid=628014439'
        df1t=pd.read_csv(url1t)
        df1t.set_index("Дата", inplace=True)
        # st.dataframe(df1t)
        df1t_b = df1t[['Баллы']]
        df1t_b['Баллы'] = df1t_b['Баллы'].str.replace(',', '.', regex=False)
        df1t_b = (df1t_b
            .rename(
                columns={'Баллы': 'Группа 1'}))


        url2t = 'https://docs.google.com/spreadsheets/d/1BQOy0f7JDxAwjd-mvKCx-l42ZoASl0IkxCGJwNyfoiI/export?format=csv&gid=628014439'
        df2t=pd.read_csv(url2t)
        # st.dataframe(df2t)
        df2t.set_index("Дата", inplace=True)
        df2t_b = df2t[['Баллы']]
        df2t_b['Баллы'] = df2t_b['Баллы'].str.replace(',', '.', regex=False)
        df2t_b = (df2t_b
            .rename(
                columns={'Баллы': 'Группа 2'}))

        # Объединяем таблицы по общему индексу
        df0t_b = df1t_b.join(df2t_b)

        today = datetime.today().date()
        yesterday = datetime.today() - timedelta(days=1)

        yesterday_str = yesterday.strftime("%Y-%m-%d")
        # st.write(yesterday_str)

        # Задаем другую дату для сравнения (например, 2023-10-01)
        other_date = datetime(2025, 2, 28).date()
        # st.text('============')
        if today <= other_date:
            df0t_b_s = df0t_b[:f'{yesterday_str}']
            # st.write("today <= other_date")
            # st.dataframe(df0t_b)
        else:
            df0t_b_s = df0t_b



        # Создание фигуры
        fig = go.Figure()

        # Добавление первого графика (Продажи)
        fig.add_trace(go.Scatter(
            x=df0t_b_s.index.to_list(), y=df0t_b_s['Группа 1'],
            mode='lines', name='Группа 1',
            line=dict(color='blue')
        ))

        # Добавление второго графика (Прибыль)
        fig.add_trace(go.Scatter(
            x=df0t_b_s.index.to_list(), y=df0t_b_s['Группа 2'],
            mode='lines', name='Группа 2',
            line=dict(color='red')
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
            st.header(f'{sel_param}')
            # st.bar_chart(df_0[sel_param])

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=df_0.index.to_list(),
                y=df_0[f'{sel_param}'],
                marker_color='skyblue'  # Цвет столбцов
            ))

            # Настройка макета
            fig.update_layout(
                title='Общий показатель',
                xaxis_title='Группы',
                yaxis_title=f'{sel_param}'
            )
            st.plotly_chart(fig, use_container_width=True)    

            # st.subheader('Лидеры групп')
            df_10 = df1.copy()
            df_10 = df_10.query('index != "Итог"') 
            df_10 = (df_10
                    .sort_values(sel_param,
                                    ascending=False)
                    .head(1)
                    )
            df_10.index = df_10.index + ' (1гр.)'
            # st.dataframe(df_10[[sel_param]].head(1))

            df_20 = df2.copy()
            df_20 = df_20.query('index != "Итог"') 
            df_20 = (df_20
                    .sort_values(sel_param, 
                                    ascending=False)
                    .head(1)
                    )
            df_20.index = df_20.index + ' (2гр.)'
            # st.dataframe(df_20[[sel_param]].head(1))

            df_00 = pd.concat([df_10, df_20])

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=df_00.index.to_list(),
                y=df_00[f'{sel_param}'],
                marker_color='skyblue'  # Цвет столбцов
            ))

            # Настройка макета
            fig.update_layout(
                title='Топы в данном показателе',
                xaxis_title='Лидеры',
                yaxis_title=f'{sel_param}'
            )
            st.plotly_chart(fig, use_container_width=True)

            # st.bar_chart(df_00[sel_param])

            df1t_p = df1t[[f'{sel_param}']]
            df1t_p = (df1t_p
                .rename(
                    columns={f'{sel_param}': 'Группа 1'}))

            df2t_p = df2t[[f'{sel_param}']]
            df2t_p = (df2t_p
                .rename(
                    columns={f'{sel_param}': 'Группа 2'}))

            df0t_p = df1t_p.join(df2t_p)

            if today <= other_date:
                df0t_p_s = df0t_p[:f'{yesterday_str}']
            else:
                df0t_p_s = df0t_p

            # Создание фигуры
            fig = go.Figure()

            # Добавление первого графика (Продажи)
            fig.add_trace(go.Scatter(
                x=df0t_p_s.index.to_list(), 
                y=df0t_p_s['Группа 1'],
                mode='lines', 
                name='Группа 1',
                line=dict(color='blue')
            ))

            # Добавление второго графика (Прибыль)
            fig.add_trace(go.Scatter(
                x=df0t_p_s.index.to_list(), 
                y=df0t_p_s['Группа 2'],
                mode='lines', 
                name='Группа 2',
                line=dict(color='red')
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


