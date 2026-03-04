# Streamlit Visualizador de Recursos-
> Projeto sujeito a atualizações

Este projeto foi desenvolvido como parte do meu aprendizado no curso de **Desenvolvimento de Sistemas**. O objetivo principal foi colocar em prática o consumo de APIs externas e a criação de dashboards interativos utilizando a linguagem Python.

---

## Propósito do Projeto
O desafio era criar uma aplicação funcional que atendesse aos seguintes critérios acadêmicos:
- Utilização de no mínimo, 2 bibliotecas externas.
- Implementação de pelo menos um gráfico para visualização de dados.
- Integração com uma fonte de dados real (API).

Utilizei o **Streamlit** para a interface, **Pandas** para tratamento dos dados, e as bibliotecas **Plotly** e **Altair** para os gráficos de distribuição e ranking.

## Tecnologias Utilizadas
- **Python**: Linguagem base.
- **Streamlit**: Framework para o dashboard.
- **Pandas**: Manipulação de tabelas / Dataframes.
- **Requests**: Consumo da API do Portal da Transparência.
- **Plotly e Altair**: Geração de gráficos interativos.

## Como rodar o projeto

Pra executar este projeto na sua máquina, siga esses passos:

### 1. Obtenha sua Chave de API
Após baixar esse repositorio no seu dispositivo, você precisará de uma chave de API do Portal da Transparência.

### 2. Configure os Segredos (Secrets)
Por questões de segurança, o código utiliza o sistema de 'secrets' do Streamlit.
- Na raiz do projeto, crie uma pasta chamada '.streamlit'.
- Dentro dela, crie um arquivo chamado 'secrets.toml'.
- Adicione sua chave no arquivo desta forma :
  ```toml
  API_KEY = "Sua chave aqui"
  ```
  
---  

# ⚠️ IMPORTANTE
Se você for clonar este repositório, se basear no código ou fazer o deploy do seu próprio projeto.
1. **Nunca suba o seu arquivo 'secrets.toml' para o GitHub.** Ele contém a sua chave privada que da acesso á API.
2. Certifique-se de que o arquivo '.streamlit/secrets.toml' está listado no seu arquivo '.gitignore'.
3. Se você enviar sua chave por engano para um repositório público, **Modifique imediatamente** no site do Portal da Transparência e gere uma nova.

*Segurança da sua API key é de sua total responsabilidade*
