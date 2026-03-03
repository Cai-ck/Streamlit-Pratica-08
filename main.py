import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import altair as alt

# Configuração da página
st.set_page_config(page_title="Portal da Transparência - Recursos Recebidos", layout="wide")

# Puxa os recursos recebidos, usando a url.
@st.cache_data
def busca_recursos_recebidos(mesAnoInicio, mesAnoFim, pagina=1):
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos"
    
    headers = {
        "chave-api-dados": st.secrets["API_KEY"], # Puxar a chave do arquivo mencionado no README.md
        "Accept": "application/json"
    }

    params = {
        "mesAnoInicio": mesAnoInicio,
        "mesAnoFim": mesAnoFim,
        "pagina": pagina
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else: #Caso simplesmente minha API der erro, ele criara dados falsos, para pelo menos demonstrar como seria os gráficos, e mostrar o erro que aconteceu na barra lateral.
            st.sidebar.error(f"Erro {response.status_code}: Usando dados de fallback.")
            return pd.DataFrame([
                {"nomePessoa": "Exemplo Estado A", "valorTotal": 150000.00, "siglaUFPessoa": "SP", "nomeOrgao": "Orgao X"},
                {"nomePessoa": "Exemplo Estado B", "valorTotal": 95000.00, "siglaUFPessoa": "RJ", "nomeOrgao": "Orgao Y"}
            ])
            
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return pd.DataFrame()

# Os filtros que vão ficar na barra lateral, ainda falta algumas adições que pretendo fazer 
with st.sidebar:
    st.header("⚙️ Filtros")
    ano = st.selectbox("Ano", [2024, 2023, 2022])
    mes = st.selectbox("Mês", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
    # intervalo_datas = st.sidebar.slider("Selecione o periodo:" min_value=mes)
    
    data_formatada = f"{mes}/{ano}"
    
    st.divider()
    cor_grafico = st.color_picker("Cor dos Gráficos", "#00f900") # Mudar a cor dos gráficos *Especificamentes as de barra

st.title("Análise de Recursos Recebidos")
st.caption(f"Período consultado: {data_formatada}")

df = busca_recursos_recebidos(data_formatada, data_formatada)

if not df.empty:
    # Caso simplesmente as colunas descritas derem erro, mude para a que a API pede.
    colunas_api = {
        'nomePessoa': 'nomeFavorecido',
        'siglaUFPessoa': 'UF',
        'nomeOrgao': 'Orgao',
        'valorTotal': 'valor'
    }
    df = df.rename(columns=colunas_api)

    if 'valor' not in df.columns:
        colunas_valor = [c for c in df.columns if 'valor' in c.lower()]
        if colunas_valor:
            df = df.rename(columns={colunas_valor[0]: 'valor'})

    # Métricas com os valores e numerações por coluna
    total = pd.to_numeric(df['valor']).sum() if 'valor' in df.columns else 0
    st.metric("Total no Período", f"R$ {total:,.2f}")
    
    aba1, aba2, aba3 = st.tabs(["Gráfico de Pizza", "Ranking", "Tabela de Dados"]) 
  
    with aba1:
        # Aba 1, gráfico de pizza, você consegue selecionar quais dados quer puxar graças ao plotly.express.

        st.subheader("Distribuição por Favorecido")
        fig_plotly = px.pie(df.head(10), names='nomeFavorecido', values='valor', 
                            title="Top 10 Favorecidos", hole=0.4)
        st.plotly_chart(fig_plotly, use_container_width=True)
  
    with aba2: # Gráfico de barras do Altair
        st.subheader("Ranking de Valores")
        chart_altair = alt.Chart(df.head(20)).mark_bar(color=cor_grafico).encode(
            x=alt.X('valor:Q', title="Valor Recebido (R$)"),
            y=alt.Y('nomeFavorecido:N', sort='-x', title="Favorecido"),
            tooltip=['nomeFavorecido', 'valor']
        ).properties(height=400)
        st.altair_chart(chart_altair, use_container_width=True)
    
    with aba3: # Apenas Dados
        st.subheader("Visualização dos Dados Brutos")
        st.dataframe(df, use_container_width=True)
else: # Caso o dado do periodo puxado não exista 
    st.warning("Nenhum dado retornado para este período.")
