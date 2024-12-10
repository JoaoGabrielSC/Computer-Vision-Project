# Trabalho 1 de Visão Computacional

Esse programa simula o comportamento de uma câmera em um ambiente tridimensional e permite controlar tanto os parâmetros extrínsecos quanto intrínsecos, possibilitando uma visualização detalhada da interação entre a câmera e o objeto.

# Exemplo de uso
![image](https://github.com/user-attachments/assets/64181102-956a-4975-95ce-0eabc0403fb9)
![image](https://github.com/user-attachments/assets/9fe156c0-47ba-447c-bc50-37e0a66a177d)
![image](https://github.com/user-attachments/assets/3b72693c-bb19-4b47-bd58-597c321434f4)

## Requisitos

- Python 3.11 ou superior.
- `pip` para gerenciar pacotes.
- `pyenv` ou `venv` para criar um ambiente virtual.
- `make` (opcional, mas recomendado para linux).

## Como rodar o projeto

### 1. Criação do ambiente virtual

Primeiro, crie e ative um ambiente virtual para o projeto. Se você estiver usando `venv`, pode seguir os seguintes passos:

**No Linux ou macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**No Windows:**

```cmd
python -m venv env
env\Scripts\activate
```
## 2. Instalação das dependências

Com o ambiente virtual ativado, instale as dependências necessárias com os seguintes comandos:

```bash
# Para linux
make install
# Para windows
pip install -r requirements.txt
```
## 3. Rodar o app

Para rodar o aplicativo, execute o seguinte comando:

```bash
# Para linux
make run
# Para windows
python main.py
```

#### Adicionando novas dependências

Se você adicionar novas dependências ao projeto, atualize o arquivo `requirements.txt` com o seguinte comando:

```bash
make add-at-requirements package=<nome-do-pacote>
```
Esse comando irá adicionar a nova dependência ao arquivo `requirements.txt` e instalar o pacote no ambiente virtual.
