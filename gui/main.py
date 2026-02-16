import tkinter as tk
import csv
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ARQUIVO_PRODUTOS = "produtos.csv"

#===================================================
# Função para carregar produtos do arquivo CSV
def carregar_produtos(caminho_arquivo):
    produtos = {}
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas[1:]:  # ignora cabeçalho
                codigo, descricao, preco = linha.strip().split(",")
                produtos[int(codigo)] = {
                    "descricao": descricao,
                    "preco": float(preco)
                }
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    return produtos

#===================================================
# Função para salvar novo produto no CSV
def salvar_produto(caminho_arquivo, descricao, preco):
    produtos = carregar_produtos(caminho_arquivo)
    novo_codigo = max(produtos.keys(), default=0) + 1
    with open(caminho_arquivo, "a", encoding="utf-8", newline="") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([novo_codigo, descricao, preco])

#===================================================
# Função para gerar recibo em PDF
def gerar_recibo(venda, cpf, forma_pagamento, data_hora):
    c = canvas.Canvas("recibo.pdf", pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, altura - 50, "Recibo de Venda - Joalheria")

    c.setFont("Helvetica", 12)
    c.drawString(50, altura - 100, f"Data/Hora: {data_hora}")
    if cpf.strip() != "":  # CPF só aparece se informado
        c.drawString(50, altura - 120, f"CPF do cliente: {cpf}")
    c.drawString(50, altura - 140, f"Forma de pagamento: {forma_pagamento}")

    c.drawString(50, altura - 180, "Produtos:")

    y = altura - 200
    total = 0
    for item in venda:
        c.drawString(60, y, f"- {item['descricao']} (R$ {item['preco']:.2f})")
        total += item['preco']
        y -= 20

    c.drawString(50, y - 20, f"Total: R$ {total:.2f}")
    c.save()

#===================================================
# Função principal
def main():
    janela = tk.Tk()
    janela.title("Sistema de Caixa - Joalheria")
    janela.geometry("600x600")

    venda = []
    forma_pagamento = None

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    label_data = tk.Label(janela, text=f"Data/Hora da venda: {data_hora}")
    label_data.pack(pady=5)

    #===================================================
    # Campo para CPF do cliente
    tk.Label(janela, text="CPF do cliente:").pack(pady=5)
    entry_cpf = tk.Entry(janela)
    entry_cpf.pack(pady=5)

    # Enter no CPF → pula para o campo de código
    def cpf_enter_event(event):
        entry_codigo.focus_set()
    entry_cpf.bind("<Return>", cpf_enter_event)

    #===================================================
    # Campo para código do produto
    label_codigo = tk.Label(janela, text="Digite o código do produto:")
    label_codigo.pack(pady=5)

    entry_codigo = tk.Entry(janela)
    entry_codigo.pack(pady=5)

    # Enter no código → adiciona produto e limpa campo
    def adicionar_produto_evento(event):
        adicionar_produto()
        entry_codigo.delete(0, tk.END)
    entry_codigo.bind("<Return>", adicionar_produto_evento)

    resumo = tk.Text(janela, height=12, width=60)
    resumo.pack(pady=10)

    #===================================================
    # Validação de CPF (opcional)
    def validar_cpf(cpf):
        if cpf.strip() == "":   # se vazio, é válido
            return True
        return cpf.isdigit() and len(cpf) == 11

    #===================================================
    # Função para adicionar produto
    def adicionar_produto():
        codigo = entry_codigo.get()
        if not codigo.isdigit():
            resumo.insert(tk.END, "Código inválido.\n")
            return
        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        codigo_int = int(codigo)
        if codigo_int in produtos:
            produto = produtos[codigo_int]
            venda.append(produto)
            resumo.insert(tk.END, f"- {produto['descricao']} (R$ {produto['preco']:.2f})\n")
        else:
            resumo.insert(tk.END, f"Produto código {codigo} não encontrado.\n")

    #===================================================
    # Função para finalizar venda
    def finalizar_venda():
        resumo.insert(tk.END, "\nResumo da venda:\n")
        total = 0
        for item in venda:
            resumo.insert(tk.END, f"- {item['descricao']} (R$ {item['preco']:.2f})\n")
            total += item['preco']
        resumo.insert(tk.END, f"Total: R$ {total:.2f}\n")

    # Botões de adicionar e finalizar
    btn_adicionar = tk.Button(janela, text="Adicionar produto", command=adicionar_produto)
    btn_adicionar.pack(pady=5)

    btn_finalizar = tk.Button(janela, text="Finalizar venda", command=finalizar_venda)
    btn_finalizar.pack(pady=5)

    #===================================================
    # Lista de produtos disponíveis
    lista_produtos = tk.Text(janela, height=8, width=60)
    lista_produtos.pack(pady=10)

    def atualizar_lista():
        lista_produtos.delete("1.0", tk.END)
        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        lista_produtos.insert(tk.END, "Produtos disponíveis:\n")
        for codigo, dados in produtos.items():
            lista_produtos.insert(tk.END, f"{codigo} - {dados['descricao']} (R$ {dados['preco']:.2f})\n")

    atualizar_lista()

    #===================================================
    # Cadastro de novos produtos
    def abrir_cadastro():
        cadastro = tk.Toplevel(janela)
        cadastro.title("Cadastrar Produto")

        tk.Label(cadastro, text="Descrição:").pack(pady=5)
        entry_desc = tk.Entry(cadastro)
        entry_desc.pack(pady=5)

        tk.Label(cadastro, text="Preço:").pack(pady=5)
        entry_preco = tk.Entry(cadastro)
        entry_preco.pack(pady=5)

        def salvar():
            descricao = entry_desc.get()
            preco = entry_preco.get()
            if descricao and preco.replace(".", "", 1).isdigit():
                salvar_produto(ARQUIVO_PRODUTOS, descricao, float(preco))
                tk.Label(cadastro, text="Produto salvo com sucesso!").pack(pady=5)
                atualizar_lista()
            else:
                tk.Label(cadastro, text="Dados inválidos.").pack(pady=5)

        tk.Button(cadastro, text="Salvar", command=salvar).pack(pady=10)

    btn_cadastrar = tk.Button(janela, text="Cadastrar produto", command=abrir_cadastro)
    btn_cadastrar.pack(pady=10)

    #===================================================
    # Função pagar
    def pagar():
        nonlocal forma_pagamento
        cpf = entry_cpf.get()
        if not validar_cpf(cpf):
            resumo.insert(tk.END, "CPF inválido.\n")
            return

        pagamento = tk.Toplevel(janela)
        pagamento.title("Forma de pagamento")

        tk.Label(pagamento, text="Escolha a forma de pagamento:").pack(pady=5)

        def confirmar(opcao):
            nonlocal forma_pagamento
            forma_pagamento = opcao
            resumo.insert(tk.END, f"Pagamento confirmado via {opcao}.\n")
            pagamento.destroy()

        tk.Button(pagamento, text="Dinheiro", command=lambda: confirmar("Dinheiro")).pack(pady=5)
        tk.Button(pagamento, text="Cartão", command=lambda: confirmar("Cartão")).pack(pady=5)
        tk.Button(pagamento, text="Pix", command=lambda: confirmar("Pix")).pack(pady=5)

    btn_pagar = tk.Button(janela, text="Pagar", command=pagar)
    btn_pagar.pack(pady=10)

        #===================================================
    # Função gerar PDF
    def gerar_pdf():
        cpf = entry_cpf.get()
        # Se o CPF for inválido (digitado mas não tem 11 dígitos), não gera recibo
        if not validar_cpf(cpf):
            resumo.insert(tk.END, "CPF inválido, não foi possível gerar recibo.\n")
            return
        # Se não houver forma de pagamento escolhida, avisa
        if not forma_pagamento:
            resumo.insert(tk.END, "Selecione forma de pagamento antes de gerar recibo.\n")
            return
        # Gera recibo normalmente (CPF só aparece se informado)
        gerar_recibo(venda, cpf, forma_pagamento, data_hora)
        resumo.insert(tk.END, "Recibo gerado em recibo.pdf\n")

    # Botão para gerar recibo PDF
    btn_recibo = tk.Button(janela, text="Gerar Recibo PDF", command=gerar_pdf)
    btn_recibo.pack(pady=10)

    #===================================================
    # Loop principal da janela
    janela.mainloop()

#===================================================
# Ponto de entrada do programa
if __name__ == "__main__":
    main()
