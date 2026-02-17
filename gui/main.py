import tkinter as tk
import csv
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkinter import messagebox

ARQUIVO_PRODUTOS = "produtos.csv"
numero_venda = 1  # contador de vendas

#===================================================
# Função para carregar produtos do arquivo CSV
def carregar_produtos(caminho_arquivo):
    produtos = {}
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas[1:]:
                partes = linha.strip().split(",")
                if len(partes) >= 3:  # garante que tenha pelo menos 3 colunas
                    codigo, descricao, preco = partes[0], partes[1], partes[2]
                    if codigo.isdigit():
                        produtos[int(codigo)] = {"descricao": descricao, "preco": float(preco)}
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
# Função para gerar recibo em PDF com numeração crescente
def gerar_recibo(venda, cpf, forma_pagamento, data_hora):
    global numero_venda
    nome_arquivo = f"recibo_{numero_venda}.pdf"
    numero_venda += 1

    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, altura - 50, "Recibo de Venda - Joalheria")
    c.setFont("Helvetica", 12)
    c.drawString(50, altura - 100, f"Data/Hora: {data_hora}")
    if cpf.strip() != "":
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
    return nome_arquivo

#===================================================
#===================================================
# Função de consulta de produtos
def abrir_consulta():
    consulta = tk.Toplevel()
    consulta.title("Consultar Produtos")
    consulta.geometry("500x400")  # tamanho inicial da janela

    tk.Label(consulta, text="Digite código ou nome:").pack(pady=5)
    entry_busca = tk.Entry(consulta, width=40)
    entry_busca.pack(pady=5)
    resultado = tk.Listbox(consulta, height=15, width=60)
    resultado.pack(pady=10)

    def mostrar_todos():
        resultado.delete(0, tk.END)
        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        for codigo, dados in produtos.items():
            resultado.insert(tk.END, f"{codigo} - {dados['descricao']} (R$ {dados['preco']:.2f})")

    def pesquisar():
        termo = entry_busca.get().strip().lower()
        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        resultado.delete(0, tk.END)
        achou = False
        for codigo, dados in produtos.items():
            if termo in str(codigo).lower() or termo in dados["descricao"].lower():
                resultado.insert(tk.END, f"{codigo} - {dados['descricao']} (R$ {dados['preco']:.2f})")
                achou = True
        if not achou:
            resultado.insert(tk.END, "Nenhum produto encontrado.")

    def adicionar_selecionado():
        selecionado = resultado.get(tk.ACTIVE)
        if "Nenhum produto" in selecionado or not selecionado.strip():
            return
        codigo = selecionado.split(" - ")[0].strip()
        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        if codigo.isdigit() and int(codigo) in produtos:
            produto = produtos[int(codigo)]
            # >>> Agora envia para a tela principal <<<
            venda.append(produto)
            resumo.insert(tk.END, f"- {produto['descricao']} (R$ {produto['preco']:.2f})\n")
            atualizar_total()
            # Popup automático
            popup = tk.Toplevel(consulta)
            popup.title("Info")
            tk.Label(popup, text="Produto enviado para a venda!").pack(padx=20, pady=20)
            popup.after(2000, popup.destroy)

    tk.Button(consulta, text="Pesquisar", command=pesquisar).pack(pady=5)
    entry_busca.bind("<Return>", lambda event: pesquisar())
    tk.Button(consulta, text="Adicionar", command=adicionar_selecionado).pack(pady=5)

    mostrar_todos()

#===================================================
# Função de cadastro de produtos
def abrir_cadastro():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastrar Produto")
    cadastro.geometry("450x350")  # tamanho inicial da janela

    frame_form = tk.Frame(cadastro, padx=20, pady=20)
    frame_form.pack(expand=True, fill="both")

    # Campo Código
    tk.Label(frame_form, text="Código do produto:").pack(anchor="w", pady=5)
    entry_codigo = tk.Entry(frame_form, width=20)
    entry_codigo.pack(pady=5)

    # Campo Descrição
    tk.Label(frame_form, text="Descrição:").pack(anchor="w", pady=5)
    entry_desc = tk.Entry(frame_form, width=40)
    entry_desc.pack(pady=5)

    # Campo Preço
    tk.Label(frame_form, text="Preço:").pack(anchor="w", pady=5)
    entry_preco = tk.Entry(frame_form, width=20)
    entry_preco.pack(pady=5)

    # Função auxiliar para popup temporário
    def mostrar_popup(mensagem):
        popup = tk.Toplevel(cadastro)
        popup.title("Info")
        tk.Label(popup, text=mensagem).pack(padx=20, pady=20)
        popup.after(2000, popup.destroy)  # fecha sozinho após 2 segundos

    # Função para validação e salvar no CSV
    def salvar():
        codigo = entry_codigo.get().strip()
        descricao = entry_desc.get().strip()
        preco = entry_preco.get().strip()

        if not codigo.isdigit():
            mostrar_popup("Erro: O código deve ser numérico.")
            return

        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        if int(codigo) in produtos:
            mostrar_popup("Erro: Já existe um produto com este código.")
            return

        if not descricao:
            mostrar_popup("Erro: A descrição não pode estar vazia.")
            return

        try:
            preco_float = float(preco)
            if preco_float <= 0:
                mostrar_popup("Erro: O preço deve ser maior que zero.")
                return
        except ValueError:
            mostrar_popup("Erro: Preço inválido. Use apenas números (ex: 12.50).")
            return

        # Salva no CSV
        with open(ARQUIVO_PRODUTOS, "a", encoding="utf-8", newline="") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow([codigo, descricao, preco_float])

        mostrar_popup("Produto salvo com sucesso!")

        # Limpa os campos
        entry_codigo.delete(0, tk.END)
        entry_desc.delete(0, tk.END)
        entry_preco.delete(0, tk.END)

    #==============================
    # Atalhos com Enter
    entry_codigo.bind("<Return>", lambda event: entry_desc.focus_set())
    entry_desc.bind("<Return>", lambda event: entry_preco.focus_set())
    entry_preco.bind("<Return>", lambda event: salvar())  # Enter no último campo já salva

    #==============================
    # Botões
    frame_botoes = tk.Frame(frame_form)
    frame_botoes.pack(pady=15)

    tk.Button(frame_botoes, text="Salvar", command=salvar, width=12).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Fechar", command=cadastro.destroy, width=12).pack(side="right", padx=10)

#===================================================
# Função principal
def main():
    janela = tk.Tk()
    janela.title("Sistema de Caixa - Joalheria")
    janela.geometry("1000x600")

# Carregar ícones da pasta icons
    icone_dinheiro = tk.PhotoImage(file="icons/vendas.png")
    icone_bolsa = tk.PhotoImage(file="icons/funil.png")
    icone_funil = tk.PhotoImage(file="icons/moeda-de-dinheiro.png")
    icone_carrinho = tk.PhotoImage(file="icons/bolsa-de-compras.png")
    icone_moeda = tk.PhotoImage(file="icons/venda-cruzada.png")

    venda = []
    forma_pagamento = None

    #==============================
    # Configuração da grid principal
    for i in range(4):
        janela.grid_columnconfigure(i, weight=1, minsize=200)
        janela.grid_rowconfigure(i, weight=1, minsize=150)
    janela.grid_rowconfigure(2, weight=3)

    #==============================
    # Coluna esquerda (16 botões em grid 4x4)
    frame_botoes = tk.Frame(janela)
    frame_botoes.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew", padx=5, pady=5)

    for i in range(4):
        frame_botoes.grid_columnconfigure(i, weight=1)
        frame_botoes.grid_rowconfigure(i, weight=1)

    #==============================
    # Botões principais
    btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar produto", image=icone_bolsa, compound="top")
    btn_cadastrar.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    btn_consultar = tk.Button(frame_botoes, text="Consultar produtos", image=icone_funil, compound="top")
    btn_consultar.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

    btn_pagar = tk.Button(frame_botoes, text="Pagar", image=icone_dinheiro, compound="top")
    btn_pagar.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)

    btn_recibo = tk.Button(frame_botoes, text="Recibo - 2ª Via", image=icone_carrinho, compound="top")
    btn_recibo.grid(row=0, column=3, sticky="nsew", padx=2, pady=2)

    for r in range(1, 4):
        for c in range(4):
            tk.Button(frame_botoes, text="Botão livre", image=icone_moeda, compound="top",).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

    #==============================
    # Coluna direita (campos principais)
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frame_info = tk.Frame(janela)
    frame_info.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
    tk.Label(frame_info, text=f"Data/Hora da venda: {data_hora}").pack(anchor="w")
    tk.Label(frame_info, text="CPF do cliente:").pack(anchor="w")
    entry_cpf = tk.Entry(frame_info)
    entry_cpf.pack(anchor="w")

    frame_codigo = tk.Frame(janela)
    frame_codigo.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
    tk.Label(frame_codigo, text="Digite o código do produto:").pack(anchor="w")
    entry_codigo = tk.Entry(frame_codigo)
    entry_codigo.pack(anchor="w")

    def cpf_enter_event(event):
        entry_codigo.focus_set()
    entry_cpf.bind("<Return>", cpf_enter_event)

    frame_produtos = tk.Frame(janela)
    frame_produtos.grid(row=2, column=3, sticky="nsew", padx=5, pady=5)
    tk.Label(frame_produtos, text="Produtos:").pack(anchor="w")
    resumo = tk.Text(frame_produtos, font=("Arial", 12))
    resumo.pack(expand=True, fill="both")

    frame_total = tk.Frame(janela)
    frame_total.grid(row=3, column=3, sticky="nsew", padx=5, pady=5)
    tk.Label(frame_total, text="Total:").pack(anchor="w")
    campo_total = tk.Text(frame_total, height=2, width=30, font=("Arial", 14, "bold"))
    campo_total.pack()
    campo_total.insert(tk.END, "Total: R$ 0.00\n")

    #==============================
    # Funções auxiliares
    def atualizar_total():
        total_venda = sum([item['preco'] for item in venda])
        campo_total.delete("1.0", tk.END)
        campo_total.insert(tk.END, f"Total: R$ {total_venda:.2f}\n")

    def validar_cpf(cpf):
        if cpf.strip() == "":
            return True
        return cpf.isdigit() and len(cpf) == 11

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
            atualizar_total()
        else:
            resumo.insert(tk.END, f"Produto código {codigo} não encontrado.\n")

    entry_codigo.bind("<Return>", lambda event: [adicionar_produto(), entry_codigo.delete(0, tk.END)])

    #==============================
    # Função de pagamento
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
            confirmacao = tk.Toplevel(janela)
            confirmacao.title("Confirmação")
            tk.Label(confirmacao, text=f"Confirmar pagamento via {opcao}?").pack(padx=20, pady=20)

            def concluir():
                nonlocal forma_pagamento
                forma_pagamento = opcao

                # Gerar recibo com numeração crescente
                nome_arquivo = gerar_recibo(venda, entry_cpf.get(), forma_pagamento, data_hora)
                resumo.insert(tk.END, f"Recibo gerado em {nome_arquivo} (1ª via)\n")

                # Popup de sucesso
                popup = tk.Toplevel(janela)
                popup.title("Sucesso")
                tk.Label(popup, text="Operação realizada com sucesso!").pack(padx=20, pady=20)
                popup.after(2000, popup.destroy)

                # >>> Limpar campos para próxima venda <<<
                venda.clear()
                resumo.delete("1.0", tk.END)
                campo_total.delete("1.0", tk.END)
                campo_total.insert(tk.END, "Total: R$ 0.00\n")
                entry_cpf.delete(0, tk.END)
                entry_codigo.delete(0, tk.END)

                confirmacao.destroy()
                pagamento.destroy()

            def cancelar():
                confirmacao.destroy()

            tk.Button(confirmacao, text="Confirmar", command=concluir).pack(side="left", padx=10, pady=10)
            tk.Button(confirmacao, text="Cancelar", command=cancelar).pack(side="right", padx=10, pady=10)

        tk.Button(pagamento, text="Dinheiro", command=lambda: confirmar("Dinheiro")).pack(pady=5)
        tk.Button(pagamento, text="Cartão", command=lambda: confirmar("Cartão")).pack(pady=5)
        tk.Button(pagamento, text="Pix", command=lambda: confirmar("Pix")).pack(pady=5)

    #==============================
    # Função para gerar segunda via do recibo
    def gerar_pdf():
        cpf = entry_cpf.get()
        if not validar_cpf(cpf):
            resumo.insert(tk.END, "CPF inválido, não foi possível gerar recibo.\n")
            return
        if not forma_pagamento:
            resumo.insert(tk.END, "Selecione forma de pagamento antes de gerar recibo.\n")
            return
        nome_arquivo = gerar_recibo(venda, cpf, forma_pagamento, data_hora)
        resumo.insert(tk.END, f"Recibo gerado em {nome_arquivo} (2ª via)\n")

    #==============================
    # Conectar botões às funções
    btn_cadastrar.config(command=abrir_cadastro)
    btn_consultar.config(command=abrir_consulta)
    btn_pagar.config(command=pagar)
    btn_recibo.config(command=gerar_pdf)

    janela.mainloop()

#===================================================
if __name__ == "__main__":
    main()
