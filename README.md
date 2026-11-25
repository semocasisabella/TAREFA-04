# TAREFA-04 - Sistema de Cadastro de Alunos (Tarefa 02)

**Disciplina:** INE5201 - Introdução à Ciência da Computação com Python  
**Aluno(s):** Nome 1 (matrícula), Nome 2 (matrícula)  
**Data:** 24/11/2026

Aplicação em Python para cadastrar e gerenciar alunos. O sistema oferece uma
interface gráfica em tons de azul e uma alternativa de uso pelo terminal.

## Funcionalidades

- Cadastrar aluno com matrícula, nome, endereço e data de nascimento.
- Listar alunos cadastrados.
- Buscar por nome ou matrícula.
- Alterar os dados de um aluno existente.
- Excluir um aluno após confirmação.
- Validar campos obrigatórios, formato de data (`dd/mm/aaaa`) e matrícula única.

## Requisitos

- Python 3 instalado.
- Tkinter disponível para usar a interface gráfica (geralmente incluído na
  instalação padrão do Python).

Não são necessárias dependências Python externas.

## Como executar

Abra um terminal nesta pasta e escolha uma das opções:

```powershell
# Interface gráfica (modo padrão)
python sistema_alunos.py

# Interface em modo texto
python sistema_alunos.py --terminal
```

No modo gráfico, preencha os campos e use os botões para cadastrar, alterar ou
excluir. Para alterar ou excluir, selecione primeiro o aluno na tabela. A busca
filtra por nome ou matrícula; o botão **Listar todos** restaura a lista completa.

No modo texto, navegue pelo menu digitando o número da operação. A opção `0`
encerra o programa.

## Dados

Os cadastros são mantidos em uma lista de dicionários somente durante a execução.
Eles não são gravados em arquivo nem banco de dados e são perdidos ao fechar o
programa.

## Arquivos

- `sistema_alunos.py`: aplicação e operações de cadastro.
- `palavras.txt`: vocabulário de termos relacionados ao sistema.

## Observações

Substitua os nomes e matrículas de exemplo no cabeçalho de `sistema_alunos.py` e
neste README pelos dados dos integrantes antes da entrega.
