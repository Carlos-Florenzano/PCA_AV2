# PCA_AV2: Sistema de Gerenciamento de Registros CRUD

---

**Desenvolvedor:** Carlos Eduardo Ingre Florenzano


## Objetivo do Sistema (Para que ele serve)

Este projeto implementa um sistema de gerenciamento de registros em Python. 
Ele resolve a necessidade de armazenar, pesquisar, editar e excluir informações de usuários de forma persistente, utilizando o arquivo `dados.csv` como base de dados.


## 🛠️ Instruções de Uso e Configuração

Siga o passo a passo para instalar as dependências e executar o programa.

### 1. Pré-requisitos

Certifique-se de que o Python 3.x está instalado em sua máquina.

### 2. Configuração do Ambiente

I.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Carlos-Florenzano/PCA_AV2
    cd PCA_AV2
    ```

II.  **Crie e Ative o Ambiente Virtual (`venv`):**
    ```bash
    # Cria o ambiente
    python3 -m venv venv

    # Ativa o ambiente (Linux/macOS)
    source venv/bin/activate
    
    # Se estiver no Windows (PowerShell), use:
    # .\venv\Scripts\activate
    ```

III.  **Instale as Dependências:**
    As dependências necessárias (Pandas, Numpy) estão listadas no `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

### 3. Como Executar

Execute o script principal do projeto:

```bash
python PCA_AV2.py