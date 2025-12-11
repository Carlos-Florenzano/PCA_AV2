import os
import pandas as pd
import numpy as np


'''
STATUS DO CÓDIGO (VERSÃO DE VERSIONAMENTO): 
- INSERIR (1): OK.
- PESQUISAR (2): OK.
- EDITAR (3): PENDENTE
'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(BASE_DIR, 'dados.csv')

# --- CABEÇALHOS ESPERADOS ---
COLUNAS_ESPERADAS = ["matricula", "nome", "idade", "num_casa", "bairro", "cidade", "uf", "telefone", "email"]
# --- FIM CABEÇALHOS ---


def editar_registro_todo():
    """
    Função Placeholder (TODO) para a Opção 3 - EDITAR/DELETAR.
    """
    return "\n>> OPÇÃO 3: EDITAR/DELETAR. FUNÇÃO AINDA NÃO IMPLEMENTADA."


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
            print(editar_registro()) # CHAMA A FUNÇÃO PENDENTE (PLACEHOLDER)
            
        elif numero_pressionado == 4:
            print("PROGRAMA ENCERRADO COM ÊXITO")
            break
            
        else:
            print("PRESSIONE UM NÚMERO QUE SEJA CORRESPONDENTE.")


def gerar_proxima_matricula():
    """
    Gera o próximo número de matrícula sequencial (Leitura robusta com header=None).
    """
    MATRICULA_INICIAL = 0 
    
    try:
        dados_permanentes = pd.read_csv(
            ARQUIVO_CSV, 
            sep=',', 
            skipinitialspace=True, 
            encoding='utf-8',
            header=None,
            names=COLUNAS_ESPERADAS
        )
        
        dados_permanentes['matricula'] = pd.to_numeric(
            dados_permanentes['matricula'], errors='coerce'
        ).fillna(-1).astype(int)
        
        if dados_permanentes.empty or dados_permanentes['matricula'].max() == -1:
             return MATRICULA_INICIAL

        ultima_matricula = dados_permanentes['matricula'].max()
        
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
        df_novo_dado.to_csv(ARQUIVO_CSV, mode='w', header=True, index=False, sep=',', encoding='utf-8')
        print(f"\n>> ARQUIVO DE DADOS CRIADO E PRIMEIRO REGISTRO SALVO (Matrícula: {matricula_gerada}).")
    else:
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
                dados_permanentes = pd.read_csv(
                    ARQUIVO_CSV, 
                    sep=',', 
                    skipinitialspace=True, 
                    encoding='utf-8', 
                    header=None, 
                    names=COLUNAS_ESPERADAS
                )
                
                dados_permanentes.columns = dados_permanentes.columns.str.strip().str.replace('"', '').str.lower()
                dados_permanentes['nome'] = dados_permanentes['nome'].astype(str).str.strip().str.lower()
                
                if 'nome' not in dados_permanentes.columns:
                     print("\n>> ERRO INESPERADO: A COLUNA 'NOME' NÃO FOI ENCONTRADA.")
                     continue
                
                nome_a_pesquisar = input("DIGITE O NOME COMPLETO QUE VOCÊ DESEJA BUSCAR: ").strip().lower()
                resultado_filtrado = dados_permanentes[dados_permanentes["nome"] == nome_a_pesquisar]

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


## Chamando o menu para que o programa inteiro possa ser inicializado:
# Passando a função PENDENTE como argumento para o menu
menu(dados_armazenados, menu_pesquisar, editar_registro_todo)