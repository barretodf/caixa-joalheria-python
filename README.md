# 💎 Sistema de Caixa - Joalheria (Versão 0.2)

Este projeto é um sistema de caixa desenvolvido em **Python** com interface gráfica em **Tkinter**.  
A versão **0.2** traz melhorias importantes em relação à versão 0.1, incluindo correções e novas funcionalidades.

## Novidades da versão 0.2
- Correção do botão **Adicionar** na consulta de produtos (agora envia corretamente para a área de venda).
- Atualização automática do **total da venda** ao adicionar produtos.
- Melhor organização da interface gráfica.
- Documentação revisada e expandida.
- Estrutura de código mais modular e clara.

## Funcionalidades principais
- Cadastro de produtos com validação.
- Consulta de produtos por código ou nome.
- Edição de produtos diretamente no CSV.
- Adição de produtos à venda com cálculo automático do total.
- Pagamento com opções: Dinheiro, Cartão e Pix.
- Geração de recibo em PDF (1ª e 2ª via).
- Interface gráfica organizada com botões e ícones.

## Tecnologias utilizadas
- **Python 3**
- **Tkinter** (interface gráfica)
- **CSV** (armazenamento dos produtos)
- **ReportLab** (geração de recibos em PDF)

## Estrutura do projeto

#======================

## ▶️ Como executar
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/caixa-joalheria-python.git

cd caixa-joalheria-python/gui

python main.py

#Para criar um executável (fica na pasta dist)

pyinstaller --onefile --windowed main.py


#============================
entre no terminal git bash.
digite:
cd Desktop/caixa-joalheria-python/gui

git checkout gui-version
python gui/main.py
#============================
ou:
abra o terminal: git bash

rode esse comando:

cd Desktop/caixa-joalheria-python

python gui/main.py
