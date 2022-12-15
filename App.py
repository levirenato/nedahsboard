import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
# data links and lists
data_m_1 = '0&single=true&output=csv'
data_m_2 = '528635708&single=true&output=csv'
data_m_3 = '1340796995&single=true&output=csv'
periodos = [dt.date(2022,12,1),]

st.title('DashBoard Sopro')
# Side bar
with st.sidebar:
    maquina = st.radio('Selecione uma Máquina',("Máquina 1","Máquina 2", "Máquina 3"), horizontal=True)

    # Select Machine   

    if maquina == "Máquina 1":
        choice_maquina = data_m_1
    elif maquina == "Máquina 2":
        choice_maquina = data_m_2
    else: choice_maquina = data_m_3

    # Load Data
    original_data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRAQFvtzFOzQLlW016jaTqjbYMd2P5Q5La8jDmEHSoFweQJLMGhjQyvUm1pw7OyhJ4arAC9ID5QIq3V/pub?gid={}'.format(choice_maquina), sep=',', index_col='Data')
    
    # date filter
    st.write('Periodo')

    coldate1,coldate2 = st.columns(2)
    with coldate1:
        de = st.date_input('De',min_value=dt.date(day=1,month=8,year=2022))
    with coldate2:
        ate = st.date_input('Até',min_value=dt.date(day=1,month=8,year=2022))

    # Filter by Date Index
    data = original_data.loc[de.strftime("%d/%m/%Y"):ate.strftime("%d/%m/%Y")]

    # Filter the oparator list and add 'all' option
    lista_operador = list(data['Operador'].drop_duplicates())
    lista_operador.insert(0,'Todos')
    filtro = st.selectbox('Operador',lista_operador,index=0)

    if filtro == "Todos":
        database = data
    else: database = data.query("Operador == '{}'".format(filtro))

    
with st.container():
    col1, col2 = st.columns(2)

    # Variables with data
    legenda = ['Produção','Inutlizado']
    inutilizado = [database['Produção'].sum(), database['Inutilizado Sopro'].sum()]

    # Machine
    st.subheader('{} :factory:'.format(maquina))
    with col1:
        # Card Inutilizado
        perda_pocem = database['Inutilizado Sopro'].sum()/(database['Produção'].sum()+database['Inutilizado Sopro'].sum())*100
        perd_und = database['Inutilizado Sopro'].sum()
        st.metric(label = '**Inutilizado** :wastebasket:', value=f"{int(perd_und)} Un", delta=f'{round(perda_pocem,2)} %',delta_color='inverse')   

    #Card Produção
    with col2:
        # Card Inutilizado
        st.metric(label = '**Produção** :gear:', value=f"{database['Produção'].sum()} Un")
    
    # Graph
    fig = go.Figure(data=[go.Pie(labels=legenda, values=inutilizado)])
    fig.update_traces(textinfo='percent',textfont_size=15)

    st.write(fig)

    # Plot Graph
    fig_week = px.line(database, x=database.index, y=["Inutilizado Sopro","Produção"], title='Produção x Inutilizado',markers=True)
    st.write(fig_week)

    st.write(database)
