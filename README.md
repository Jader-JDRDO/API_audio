# 🎙️ Orenda Voice Stock: Automação de Estoque por Comando de Voz (Projeto experimental)

O Orenda Voice Stock é um script inteligente desenvolvido em Python para otimização de fluxos logísticos e gerenciamento de inventário. O sistema utiliza captura e transcrição de áudio em tempo real, processamento de texto via Expressões Regulares (Regex), manipulação de dados com Pandas e persistência em banco de dados relacional SQLite.

O objetivo do projeto é substituir o preenchimento manual de planilhas por uma interface de voz ágil, reduzindo o tempo de operação e eliminando erros de digitação no cotidiano de gestão de mercadorias.

🛠️ Tecnologias e Bibliotecas Utilizadas

*   Python 3 (Linguagem base do ecossistema)
*   SpeechRecognition (Captura de áudio do microfone e integração com a API de Speech-to-Text do Google)
*   SQLite3 (Banco de dados relacional local para persistência estável)
*   Pandas (Estruturação, leitura de queries SQL e exibição organizada dos dados em formato tabular)
*   Regex (re) (Filtragem e extração precisa de padrões de texto)

⚙️ Como o Sistema Funciona

O fluxo do programa foi desenhado em três etapas sequenciais:

1.  Captura e Transcrição (Voice-to-Text): O script calibra o microfone para isolar ruídos de fundo e aguarda o comando de voz em português (Ex: "maçã 3 unidades, banana 4 unidades"). O áudio é enviado e transcrito instantaneamente.
2.  Processamento de Linguagem com Regex: O texto bruto é tratado por uma expressão regular que identifica os blocos de produtos e suas respectivas quantidades numéricas, limpando palavras sobressalentes (como "unidade" ou "unidades") e isolando as variáveis necessárias.
3.  Inteligência de Banco de Dados (SQL): 
       Caso o produto já exista na tabela, o script realiza um `UPDATE`, somando incrementalmente a nova quantidade ao saldo atual.
       Caso seja um item inédito, o script gera automaticamente uma chave primária única (`codigo_produto`) baseada em um timestamp e nas iniciais do produto, executando um `INSERT`.
4.  Exibição Tabular: O Pandas faz a leitura direta do banco de dados via query e imprime no terminal a posição consolidada e atualizada do estoque.

📁 Estrutura do Banco de Dados (`estoque`)

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `codigo_produto` | TEXT (PK) | Chave primária gerada dinamicamente (`PROD_[TIMESTAMP]_[INICIAIS]`) |
| `nome` | TEXT (Unique) | Nome limpo do item cadastrado |
| `quantidade` | INTEGER | Saldo atualizado do produto em estoque |
| `ultima_atualizacao`| TEXT | Timestamp da última modificação do registro |

🚀 Como Executar o Projeto

Pré-requisitos
Certifique-se de ter o Python instalado e um microfone configurado no sistema. Instale as dependências executando no terminal:  
  pip install PyAudio SpeechRecognition pandas
