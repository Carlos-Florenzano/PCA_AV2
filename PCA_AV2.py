import os
import pandas as pd
import numpy as np


'''
STATUS DO CÓDIGO (11/12/2025): 
- INSERIR (1): OK.
- PESQUISAR (2): OK, com correção de leitura (header=None) e limpeza de strings.
- EDITAR (3): Implementado e funcional.
'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(BASE_DIR, 'dados.csv')

# --- CABEÇALHOS ESPERADOS ---
COLUNAS_ESPERADAS = ["matricula", "nome", "idade", "num_casa", "bairro", "cidade", "uf", "telefone", "email"]
# --- FIM CABEÇALHOS ---


def menu(dados_armazenados, menu_pesquisar, editar_registro):
    while True:
        print("MENU:\n" + "PRESSIONE:\n" + "1 - INSERIR\n" + "2 - PESQUISAR\n" + "3 - EDITAR\n" + "4 - SAIR\n" + "--------------------"
        + "--------\n")
        
        try:
            numero_pressionado = int(input("~ :"))
        except ValueError:
            print(">> ERRO: POR FAVOR, DIGITE APENAS UM NÚMERO.")
            continue

        if numero_pressionado == 1:
            print(dados_armazenados())
        
        elif numero_pressionado == 2:
            print(menu_pesquisar())

        elif numero_pressionado == 3:
            print(editar_registro()) # CHAMADA PARA A FUNÇÃO DE EDIÇÃO
            
        elif numero_pressionado == 4:
            print("PROGRAMA ENCERRADO COM ÊXITO")
            break # break pra fechar o programa
            
        else:
            print("POR FAVOR DIGITE CORRETAMENTE PARA A FUNÇÃO DESEJADA.")


def gerar_proxima_matricula():
    """
    Gera o próximo número de matrícula sequencial lendo o último
    registro no arquivo CSV.
    CORRIGIDO: Leitura robusta com header=None para evitar o bug do 'nan'.
    """
    MATRICULA_INICIAL = 0 
    
    try:
        # CORREÇÃO: Usando a leitura robusta (header=None)
        dados_permanentes = pd.read_csv(
            ARQUIVO_CSV, 
            sep=',', 
            skipinitialspace=True, 
            encoding='utf-8',
            header=None,
            names=COLUNAS_ESPERADAS
        )
        
        # Limpa e converte a coluna antes de buscar o máximo
        # O preenchimento com -1 ajuda a garantir que o max() não retorne 0 se o arquivo estiver vazio
        dados_permanentes['matricula'] = pd.to_numeric(
            dados_permanentes['matricula'], errors='coerce'
        ).fillna(-1).astype(int)
        
        # Se o DataFrame estiver vazio após a leitura, retorna a inicial
        if dados_permanentes.empty or dados_permanentes['matricula'].max() == -1:
             return MATRICULA_INICIAL

        # Usa .max() para encontrar o maior número de matrícula
        ultima_matricula = dados_permanentes['matricula'].max()
        
        # Retorna a próx. matrícula
        return ultima_matricula + 1
        
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return MATRICULA_INICIAL
    except Exception as e:
        print(f"Erro ao gerar matrícula: {e}")
        return MATRICULA_INICIAL

def dados_armazenados():
    dados = {}
    
    matricula_gerada = gerar_proxima_matricula()
    dados["matricula"] = matricula_gerada 
    
    print(f"\n>> NOVO REGISTRO - MATRÍCULA: {matricula_gerada}")
    
    # Coleta os demais dados, usando .strip().lower() para limpeza
    dados["nome"] = input("DIGITE SEU NOME: \n").strip().lower()
    dados["idade"] = input("DIGITE SUA IDADE: \n") 
    
    try:
        dados["num_casa"] = int(input("DIGITE SEU NÚMERO DA RESIDÊNCIA: \n"))
        dados["telefone"] = int(input("DIGITE SEU NÚMERO DE TELEFONE: \n"))
    except ValueError:
        print("ATENÇÃO: NÚMERO DA CASA OU TELEFONE INVÁLIDO, USANDO 0.")
        dados["num_casa"] = 0
        dados["telefone"] = 0
        
    dados["bairro"] = input("DIGITE SEU BAIRRO: \n").strip().lower()
    dados["cidade"] = input("DIGITE A SUA CIDADE: \n").strip().lower()
    dados["uf"] = input("DIGITE O SEU ESTADO: \n").strip().lower()
    dados["email"] = input("DIGITE O SEU EMAIL: \n").strip().lower()
    
    COLUNAS = COLUNAS_ESPERADAS # Garante a ordem das colunas
    
    df_novo_dado = pd.DataFrame([dados], columns=COLUNAS) 
    
    # Lógica para anexar/salvar
    if not os.path.isfile(ARQUIVO_CSV) or os.path.getsize(ARQUIVO_CSV) == 0:
        # CRIAÇÃO GARANTIDA: Se o arquivo NÃO EXISTE, cria com cabeçalho
        df_novo_dado.to_csv(ARQUIVO_CSV, mode='w', header=True, index=False, sep=',', encoding='utf-8')
        print(f"\n>> ARQUIVO DE DADOS CRIADO E PRIMEIRO REGISTRO SALVO (Matrícula: {matricula_gerada}).")
    else:
        # Anexar: Se o arquivo existe, anexa sem cabeçalho
        df_novo_dado.to_csv(ARQUIVO_CSV, mode='a', header=False, index=False, sep=',', encoding='utf-8')
        print(f"\n>> NOVO REGISTRO DE {dados['nome']} (Matrícula: {matricula_gerada}) ADICIONADO AO ARQUIVO.")

    return "INSERÇÃO DE DADOS FINALIZADA."

def menu_pesquisar():
    while True: 
        print("\nO QUE VOCÊ DESEJA PESQUISAR?\n" + 
              "1 - NOME\n" + 
              "2 - MATRÍCULA\n" + 
              "3 - VOLTAR\n" + 
              "-----------------------\n")
        
        try:
            numero_pressionado = int(input("~ :"))
        except ValueError:
            print(">> ERRO: POR FAVOR, DIGITE APENAS UM NÚMERO PARA A OPÇÃO.")
            continue

        if numero_pressionado == 1:
            try:
                # LER: CORRIGIDO com header=None
                dados_permanentes = pd.read_csv(
                    ARQUIVO_CSV, 
                    sep=',', 
                    skipinitialspace=True, 
                    encoding='utf-8', 
                    header=None, 
                    names=COLUNAS_ESPERADAS
                )
                
                # Garante que as colunas lidas sejam limpas (embora names já as defina)
                dados_permanentes.columns = dados_permanentes.columns.str.strip().str.replace('"', '').str.lower()
                
                # CORREÇÃO DEFINITIVA: Limpeza do conteúdo da COLUNA 'NOME' no DataFrame
                dados_permanentes['nome'] = dados_permanentes['nome'].astype(str).str.strip().str.lower()
                
                if 'nome' not in dados_permanentes.columns:
                     print("\n>> ERRO INESPERADO: A COLUNA 'NOME' NÃO FOI ENCONTRADA MESMO COM A CORREÇÃO.")
                     continue
                
                # Filtragem: O input do usuário também é limpo e padronizado
                nome_a_pesquisar = input("DIGITE O NOME COMPLETO QUE VOCÊ DESEJA BUSCAR: ").strip().lower()
                resultado_filtrado = dados_permanentes[dados_permanentes["nome"] == nome_a_pesquisar]

                # Imprime o resultado
                if resultado_filtrado.empty:
                    print(f"\n>> NENHUM REGISTRO ENCONTRADO PARA O NOME: {nome_a_pesquisar}")
                else:
                    print(f"\n--- RESULTADO DA PESQUISA PARA: '{nome_a_pesquisar}' ---")
                    print(resultado_filtrado.to_string(index=False))

            except pd.errors.EmptyDataError:
                print("\n>> ARQUIVO DE DADOS VAZIO. INSIRA UM REGISTRO PRIMEIRO (OPÇÃO 1).")
            except FileNotFoundError:
                print("\n>> ERRO: O ARQUIVO DE DADOS NÃO FOI ENCONTRADO.")
            
            
        elif numero_pressionado == 2:
            try:
                # LER: CORRIGIDO com header=None
                dados_permanentes = pd.read_csv(
                    ARQUIVO_CSV, 
                    sep=',', 
                    skipinitialspace=True, 
                    encoding='utf-8', 
                    header=None, 
                    names=COLUNAS_ESPERADAS
                )
                
                dados_permanentes.columns = dados_permanentes.columns.str.strip().str.replace('"', '').str.lower()
                
                if 'matricula' in dados_permanentes.columns:
                    # Converte para numérico, preenchendo erros com -1
                    dados_permanentes['matricula'] = pd.to_numeric(
                        dados_permanentes['matricula'], errors='coerce'
                    ).fillna(-1).astype(int)
                else:
                    print("\n>> ERRO: A COLUNA 'MATRICULA' NÃO FOI ENCONTRADA.")
                    continue

                matricula_input = input("DIGITE O NÚMERO DE MATRÍCULA DESEJADO PARA A BUSCA: ")
                
                try:
                    matricula_a_pesquisar = int(matricula_input)
                except ValueError:
                    print("\n>> POR FAVOR, DIGITE APENAS NÚMEROS PARA A MATRÍCULA.")
                    continue
                    
                resultado_filtrado = dados_permanentes[dados_permanentes["matricula"] == matricula_a_pesquisar]

                if resultado_filtrado.empty:
                    print(f"\n>> NENHUM REGISTRO ENCONTRADO PARA A MATRÍCULA: {matricula_a_pesquisar}")
                else:
                    print(f"\n--- RESULTADO DA PESQUISA PARA A MATRÍCULA '{matricula_a_pesquisar}' ---")
                    print(resultado_filtrado.to_string(index=False)) 

            except pd.errors.EmptyDataError:
                print("\n>> ARQUIVO DE DADOS VAZIO. INSIRA UM REGISTRO PRIMEIRO (OPÇÃO 1 DO MENU INICIAL).")
            except FileNotFoundError:
                print("\n>> ERRO: O ARQUIVO DE DADOS NÃO FOI ENCONTRADO.")

        elif numero_pressionado == 3:
            return 
            
        else:
            print("PRESSIONE UM NÚMERO QUE SEJA CORRESPONDENTE.")

def editar_registro():
    """
    Permite ao usuário buscar um registro por matrícula e modificar seus campos.
    """
    
    print("\n--- INICIAR EDIÇÃO DE REGISTRO ---")
    
    # 1. Solicitar a matrícula para buscar o registro
    try:
        matricula_input = input("DIGITE A MATRÍCULA DO REGISTRO QUE DESEJA EDITAR: ")
        matricula_a_editar = int(matricula_input)
    except ValueError:
        return ">> ERRO: MATRÍCULA DEVE SER UM NÚMERO."
    
    try:
        # 2. Ler o arquivo completo (com header=None)
        dados_permanentes = pd.read_csv(
            ARQUIVO_CSV, 
            sep=',', 
            skipinitialspace=True, 
            encoding='utf-8', 
            header=None, 
            names=COLUNAS_ESPERADAS
        )
        dados_permanentes.columns = dados_permanentes.columns.str.strip().str.replace('"', '').str.lower()
        
        # Garante que a coluna matrícula é numérica para comparação
        dados_permanentes['matricula'] = pd.to_numeric(
            dados_permanentes['matricula'], errors='coerce'
        ).fillna(-1).astype(int)
        
        # 3. Localizar a linha
        registro_index = dados_permanentes[dados_permanentes['matricula'] == matricula_a_editar].index
        
        if registro_index.empty:
            return f">> ERRO: REGISTRO COM MATRÍCULA {matricula_a_editar} NÃO ENCONTRADO."
        
        # Indexa o registro único (retorna o índice da linha)
        idx = registro_index[0]
        
        print("\nREGISTRO ATUAL:")
        # Imprime o registro formatado, pulando a matrícula
        print(dados_permanentes.loc[idx, COLUNAS_ESPERADAS[1:]].to_string())
        print("----------------------------")
        
        # 4. Oferecer opções de edição
        campos_editaveis = COLUNAS_ESPERADAS[1:] # Todos os campos exceto 'matricula'
        
        for campo in campos_editaveis:
            valor_atual = dados_permanentes.loc[idx, campo]
            
            # Garante que o valor atual é uma string limpa para exibição (necessário se for nan ou float)
            valor_display = str(valor_atual).strip().lower()
            if valor_display == 'nan':
                 valor_display = 'VAZIO'
            
            novo_valor = input(
                f"EDITAR '{campo.upper()}' (ATUAL: {valor_display}) | DIGITE NOVO VALOR OU DEIXE EM BRANCO PARA MANTER: \n~ : "
            ).strip()
            
            if novo_valor:
                # Trata números (idade, num_casa, telefone)
                if campo in ['idade', 'num_casa', 'telefone']:
                    try:
                        novo_valor = int(novo_valor)
                    except ValueError:
                        print(f">> ATENÇÃO: VALOR INVÁLIDO PARA {campo.upper()}. VALOR ORIGINAL MANTIDO.")
                        continue
                
                # Padroniza strings
                elif campo in ['nome', 'bairro', 'cidade', 'uf', 'email']:
                    # Padroniza apenas o nome/localidades para minúsculas
                    if campo in ['nome', 'bairro', 'cidade', 'uf']:
                        novo_valor = novo_valor.lower()
                    
                # Aplica a mudança no DataFrame
                dados_permanentes.loc[idx, campo] = novo_valor
                print(f">> CAMPO '{campo.upper()}' ATUALIZADO PARA: {novo_valor}")

        # 5. Salvar o DataFrame completo (sobrescrever)
        # CORREÇÃO: Sobrescreve o arquivo com o DataFrame completo, sempre com cabeçalho
        dados_permanentes.to_csv(ARQUIVO_CSV, mode='w', header=True, index=False, sep=',', encoding='utf-8')
        
        return f"\n>> SUCESSO! REGISTRO (MATRÍCULA {matricula_a_editar}) FOI ATUALIZADO E SALVO."
        
    except pd.errors.EmptyDataError:
        return "\n>> ARQUIVO DE DADOS VAZIO. NADA PARA EDITAR."
    except FileNotFoundError:
        return "\n>> ERRO: O ARQUIVO DE DADOS NÃO FOI ENCONTRADO."
    except Exception as e:
        return f"\n>> ERRO INESPERADO DURANTE A EDIÇÃO: {e}"


## Chamando o menu para que o programa inteiro possa ser inicializado:
menu(dados_armazenados, menu_pesquisar, editar_registro)