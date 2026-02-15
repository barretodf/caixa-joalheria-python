# Sistema de Venda - Joalheria (Versão 1.0)

## Descrição
Sistema de vendas simples em **Python**, rodando no **terminal**, que utiliza um arquivo CSV para carregar os produtos disponíveis.  
O objetivo é simular um caixa de joalheria, permitindo buscar produtos, adicionar itens à venda e calcular o total automaticamente.

---

## Funcionalidades
- **Leitura de produtos do CSV**  
- **Busca por código**  
- **Adicionar item à venda (múltiplos produtos)**  
- **Cálculo automático do total**  
- **Finalizar venda digitando `0`**  
- **Validações básicas**  
  - Bloqueio de letras e símbolos em campos numéricos  
  - Impede códigos inexistentes ou negativos  
  - Evita finalizar venda sem produtos  

---

## Estrutura do Projeto

---

## Exemplo de Uso
```bash
$ python main.py
=== SISTEMA DE CAIXA - JOALHERIA ===

Produtos disponíveis:
1010 - Anel de Ouro (R$ 1200.00)
1011 - Colar de Prata (R$ 350.00)
...

Digite o código do produto (ou '0' para finalizar): 1010
Produto: Anel de Ouro - Preço: R$ 1200.00

Digite o código do produto (ou '0' para finalizar): 1011
Produto: Colar de Prata - Preço: R$ 350.00

Digite o código do produto (ou '0' para finalizar): 0

Resumo da venda:
- Anel de Ouro (R$ 1200.00)
- Colar de Prata (R$ 350.00)
Total da venda: R$ 1550.00


## Como rodar

git clone <url-do-repo>
cd caixa-joalheria-python
python main.py
