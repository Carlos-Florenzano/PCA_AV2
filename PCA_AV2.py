import os
import pandas as pd
import numpy as np


'''
STATUS DO CÓDIGO (11/12/2025 - Versão com Exclusão): 
- INSERIR (1): OK.
- PESQUISAR (2): OK.
- EDITAR/DELETAR (3): OK (Além da opção de editar, agora temos a de excluir o registro inteiro).
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
            break
            
        else:
            print("PRESSIONE UM NÚMERO QUE SEJA CORRESPONDENTE.")


def gerar_proxima_matricula():
    """
    Gera o próximo número de matrícula sequencial lendo o último
    registro no arquivo CSV (leitura robusta com header=None).
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
        
        # Converte a coluna antes de buscar o máximo
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

def editar_registro():
    """
    Permite ao usuário buscar um registro por matrícula para editar, apagar campos ou deletar o registro inteiro.
    Comandos especiais: DIGITAR 'APAGAR' para deletar o campo.
    """
    
    print("\n--- INICIAR EDIÇÃO DE REGISTRO ---")
    
    # 1. Escolha de Ação
    print("AÇÕES DISPONÍVEIS:")
    print("1 - EDITAR CAMPOS ESPECÍFICOS (OU APAGAR UM CAMPO)")
    print("2 - EXCLUIR REGISTRO INTEIRO")
    print("3 - VOLTAR\n")
    
    try:
        acao = int(input("~ : ").strip())
    except ValueError:
        return ">> ERRO: POR FAVOR, DIGITE APENAS O NÚMERO DA AÇÃO DESEJADA."

    if acao == 3:
        return "" # Volta ao menu principal
    
    # 2. Solicitar a matrícula para buscar o registro
    try:
        matricula_input = input("\nDIGITE A MATRÍCULA DO REGISTRO QUE DESEJA MANIPULAR: ")
        matricula_a_manipular = int(matricula_input)
    except ValueError:
        return ">> ERRO: MATRÍCULA DEVE SER UM NÚMERO."
    
    try:
        # 3. Ler o arquivo completo
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
        
        # 4. Localizar a linha
        registro_index = dados_permanentes[dados_permanentes['matricula'] == matricula_a_manipular].index
        
        if registro_index.empty:
            return f">> ERRO: REGISTRO COM MATRÍCULA {matricula_a_manipular} NÃO ENCONTRADO."
        
        idx = registro_index[0]
        
        # --- AÇÃO 2: EXCLUSÃO DE REGISTRO INTEIRO ---
        if acao == 2:
            print(f"\n--- EXCLUSÃO PERMANENTE DO REGISTRO MATRÍCULA {matricula_a_manipular} ---")
            confirmacao = input("CONFIRMAR EXCLUSÃO PERMANENTE? (DIGITE 'SIM'): ").strip().upper()
            
            if confirmacao == 'SIM':
                # Deleta a linha do DataFrame
                dados_permanentes = dados_permanentes.drop(index=idx).reset_index(drop=True)
                
                # Sobrescreve o arquivo com a exclusão
                dados_permanentes.to_csv(ARQUIVO_CSV, mode='w', header=True, index=False, sep=',', encoding='utf-8')
                return f"\n>> SUCESSO! REGISTRO (MATRÍCULA {matricula_a_manipular}) FOI EXCLUÍDO DEFINITIVAMENTE."
            else:
                return ">> AÇÃO CANCELADA PELO USUÁRIO."

        # --- AÇÃO 1: EDIÇÃO DE CAMPOS ESPECÍFICOS ---
        elif acao == 1:
            print("\nREGISTRO ATUAL:")
            print(dados_permanentes.loc[idx, COLUNAS_ESPERADAS[1:]].to_string())
            print("------------------------------------------------------------------------------------------------------")
            print("DICAS: DIGITE 'APAGAR' para remover o valor de um campo | Deixe em branco (Enter) para manter o valor atual")
            print("----------------------------")
            
            campos_editaveis = COLUNAS_ESPERADAS[1:] # Todos os campos exceto 'matricula'
            
            for campo in campos_editaveis:
                valor_atual = dados_permanentes.loc[idx, campo]
                
                valor_display = str(valor_atual).strip().lower()
                if valor_display == 'nan':
                    valor_display = 'VAZIO'
                
                novo_valor_input = input(
                    f"EDITAR '{campo.upper()}' (ATUAL: {valor_display}) | NOVO VALOR, APAGAR ou ENTER: \n~ : "
                ).strip()
                
                if novo_valor_input.upper() == 'APAGAR':
                    # Ação de deletar o valor do campo (NaN no Pandas)
                    dados_permanentes.loc[idx, campo] = np.nan
                    print(f">> CAMPO '{campo.upper()}' FOI APAGADO.")
                    continue
                
                if novo_valor_input:
                    # Substituição do valor
                    
                    if campo in ['idade', 'num_casa', 'telefone']:
                        try:
                            novo_valor = int(novo_valor_input)
                        except ValueError:
                            print(f">> ATENÇÃO: VALOR INVÁLIDO PARA {campo.upper()} (ESPERADO NÚMERO). VALOR ORIGINAL MANTIDO.")
                            continue
                    
                    elif campo in ['nome', 'bairro', 'cidade', 'uf']:
                        novo_valor = novo_valor_input.lower()
                    else: # email, etc.
                        novo_valor = novo_valor_input
                        
                    # Aplica a mudança no DataFrame
                    dados_permanentes.loc[idx, campo] = novo_valor
                    print(f">> CAMPO '{campo.upper()}' ATUALIZADO PARA: {novo_valor_input}")

            # 5. Salvar o DataFrame completo (sobrescrever)
            dados_permanentes.to_csv(ARQUIVO_CSV, mode='w', header=True, index=False, sep=',', encoding='utf-8')
            
            return f"\n>> SUCESSO! REGISTRO (MATRÍCULA {matricula_a_manipular}) FOI ATUALIZADO E SALVO."
        
        else:
            return ">> OPÇÃO INVÁLIDA NO MENU DE AÇÕES."
        
    except pd.errors.EmptyDataError:
        return "\n>> ARQUIVO de DADOS VAZIO. NADA PARA EDITAR."
    except FileNotFoundError:
        return "\n>> ERRO: O ARQUIVO DE DADOS NÃO FOI ENCONTRADO."
    except Exception as e:
        return f"\n>> ERRO INESPERADO DURANTE A EDIÇÃO: {e}"


## Chamando o menu para que o programa inteiro possa ser inicializado:
menu(dados_armazenados, menu_pesquisar, editar_registro)