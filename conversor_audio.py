import datetime
import re
import sqlite3
import speech_recognition as sr
import pandas as pd

# 1. FUNÇÃO PARA GRAVAR E TRANSCREVER O ÁUDIO
def transcrever_audio():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Orenda] Ajustando ruído de fundo... Aguarde.")
        reconhecedor.adjust_for_ambient_noise(source, duration=1)
        print("Pode falar os produtos e quantidades (Ex: maçã 3 unidades, banana 4 unidades)...")
        
        try:
            # Grava o áudio do microfone
            audio = reconhecedor.listen(source, timeout=5)
            print("Processando o áudio com o nosso tempo Kairós...")
            
            # Transcreve usando a API do Google (em português)
            texto = reconhecedor.recognize_google(audio, language="pt-BR")
            print(f"Texto transcrito: '{texto}'")
            return texto.lower()
            
        except sr.UnknownValueError:
            print("Não consegui entender o áudio. Tente falar mais claro.")
            return None
        except sr.RequestError:
            print("Erro de conexão com o serviço de transcrição.")
            return None

# 2. FUNÇÃO PARA TRATAR O TEXTO E EXTRAIR PRODUTOS E QUANTIDADES
def extrair_dados(texto):
    # Usando Expressões Regulares (Regex) para capturar o padrão: "nome do produto" + "número"
    # Exemplo de texto: "maçã 3 unidades banana 4 unidades" ou "maçã 3 banana 4"
    padrao = re.findall(r'([a-zA-Záéíóúàèìòùâêîôûãõç\s]+?)\s+(\d+)', texto)
    
    produtos_processados = []
    for item, qtd in padrao:
        nome_produto = item.strip().replace("unidades", "").replace("unidade", "").strip()
        if nome_produto:
            produtos_processados.append({
                "produto": nome_produto,
                "quantidade": int(qtd)
            })
    return produtos_processados

# 3. FUNÇÃO PARA ATUALIZAR O BANCO DE DADOS (SQLITE)
def atualizar_estoque(lista_produtos):
    # Conecta ao banco local (se não existir, ele cria o arquivo automaticamente)
    conn = sqlite3.connect('estoque_logistica.db')
    cursor = conn.cursor()
    
    # Cria a tabela se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            codigo_produto TEXT PRIMARY KEY,
            nome TEXT UNIQUE,
            quantidade INTEGER,
            ultima_atualizacao TEXT
        )
    ''')
    
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for item in lista_produtos:
        nome = item['produto']
        qtd = item['quantidade']
        
        # Verifica se o produto já existe no banco
        cursor.execute("SELECT quantidade FROM estoque WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()
        
        if resultado:
            # UPDATE: Se já existe, soma a nova quantidade
            nova_qtd = resultado[0] + qtd
            cursor.execute('''
                UPDATE estoque 
                SET quantidade = ?, ultima_atualizacao = ? 
                WHERE nome = ?
            ''', (nova_qtd, data_atual, nome))
            print(f"🔄 Estoque atualizado: {nome} -> +{qtd} unidades (Total: {nova_qtd})")
        else:
            # INSERT: Se é novo, gera um código novo baseado no timestamp e cadastra
            codigo_novo = f"PROD_{int(datetime.datetime.now().timestamp())}_{nome[:3].upper()}"
            cursor.execute('''
                INSERT INTO estoque (codigo_produto, nome, quantidade, ultima_atualizacao)
                VALUES (?, ?, ?, ?)
            ''', (codigo_novo, nome, qtd, data_atual))
            print(f"✨ Novo produto cadastrado: {nome} (Código: {codigo_novo}) com {qtd} unidades.")
            
    conn.commit()
    
    # Usando PANDAS para exibir como ficou o banco de dados final bem organizado
    df = pd.read_sql_query("SELECT * FROM estoque", conn)
    print("\n--- POSIÇÃO ATUAL DO ESTOQUE ---")
    print(df.to_string(index=False))
    
    conn.close()

# --- EXECUÇÃO DO PROGRAMA ---
if __name__ == "__main__":
    # Usando Carpe Diem: vamos rodar o fluxo no momento presente
    texto_gravado = transcrever_audio()
    
    # Se você não tiver microfone agora, pode descomentar a linha abaixo para testar com texto:
    # texto_gravado = "maçã 3 unidades banana 5 unidades chuchu 2"
    
    if texto_gravado:
        dados_finais = extrair_dados(texto_gravado)
        if dados_finais:
            atualizar_estoque(dados_finais)
        else:
            print("Nenhum produto ou quantidade foi identificado no texto.")