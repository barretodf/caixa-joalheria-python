import tkinter as tk
import csv
from datetime import datetime

ARQUIVO_PRODUTOS = "produtos.csv"

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

def salvar_produto(caminho_arquivo, descricao, preco):
    produtos = carregar_produtos(caminho_arquivo)
    novo_codigo = max(produtos.keys(), default=0) + 1
    with open(caminho_arquivo, "a", encoding="utf-8", newline="") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([novo_codigo, descricao, preco])

def main():
    # Criar janela principal
    janela = tk.Tk()
    janela.title("Sistema de Caixa - Joalheria")
    janela.geometry("600x500")

    # Lista de venda (armazenar produtos adicionados)
    venda = []

    # Mostrar data/hora da venda
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    label_data = tk.Label(janela, text=f"Data/Hora da venda: {data_hora}")
    label_data.pack(pady=5)

    # Campo CPF
    tk.Label(janela, text="CPF do cliente:").pack(pady=5)
    entry_cpf = tk.Entry(janela)
    entry_cpf.pack(pady=5)

    # Label de instrução
    label_codigo = tk.Label(janela, text="Digite o código do produto:")
    label_codigo.pack(pady=5)

    # Campo de entrada
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack(pady=5)

    # Área de resumo (produtos e total)
    resumo = tk.Text(janela, height=12, width=60)
    resumo.pack(pady=10)

    # Função para adicionar produto
    def adicionar_produto():
        codigo = entry_codigo.get()

        if not codigo.isdigit():
            resumo.insert(tk.END, "Código inválido, digite apenas números.\n")
            return

        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        codigo_int = int(codigo)
        if codigo_int in produtos:
            produto = produtos[codigo_int]
            resumo.insert(tk.END, f"{produto['descricao']} adicionado.\n")
            venda.append(produto)
        else:
            resumo.insert(tk.END, f"Produto código {codigo} não encontrado.\n")

    # Função para finalizar venda
    def finalizar_venda():
        resumo.insert(tk.END, "\nResumo da venda:\n")
        total = 0
        for item in venda:
            resumo.insert(tk.END, f"- {item['descricao']} (R$ {item['preco']:.2f})\n")
            total += item['preco']
        resumo.insert(tk.END, f"Total: R$ {total:.2f}\n")

    # Botão "Adicionar produto"
    btn_adicionar = tk.Button(janela, text="Adicionar produto", command=adicionar_produto)
    btn_adicionar.pack(pady=5)

    # Botão "Finalizar venda"
    btn_finalizar = tk.Button(janela, text="Finalizar venda", command=finalizar_venda)
    btn_finalizar.pack(pady=5)

    # ====================================
    # O próximo código vai aqui
    # ====================================

    # Área para listar produtos disponíveis
    lista_produtos = tk.Text(janela, height=8, width=60)
    lista_produtos.pack(pady=10)

    def atualizar_lista():
        lista_produtos.delete("1.0", tk.END)
        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        lista_produtos.insert(tk.END, "Produtos disponíveis:\n")
        for codigo, dados in produtos.items():
            lista_produtos.insert(tk.END, f"{codigo} - {dados['descricao']} (R$ {dados['preco']:.2f})\n")

    atualizar_lista()

    # Função para abrir janela de cadastro
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

    # Botão principal para abrir cadastro
    btn_cadastrar = tk.Button(janela, text="Cadastrar produto", command=abrir_cadastro)
    btn_cadastrar.pack(pady=10)

    # Função para validar CPF
    def validar_cpf(cpf):
        return cpf.isdigit() and len(cpf) == 11

    # Função para abrir opções de pagamento
    def pagar():
        cpf = entry_cpf.get()
        if not validar_cpf(cpf):
            resumo.insert(tk.END, "CPF inválido. Digite 11 números.\n")
            return

        pagamento = tk.Toplevel(janela)
        pagamento.title("Forma de pagamento")

        tk.Label(pagamento, text="Escolha a forma de pagamento:").pack(pady=5)

        def confirmar(opcao):
            resumo.insert(tk.END, f"Pagamento confirmado via {opcao}.\n")
            pagamento.destroy()

        tk.Button(pagamento, text="Dinheiro", command=lambda: confirmar("Dinheiro")).pack(pady=5)
        tk.Button(pagamento, text="Cartão", command=lambda: confirmar("Cartão")).pack(pady=5)
        tk.Button(pagamento, text="Pix", command=lambda: confirmar("Pix")).pack(pady=5)

    # Botão Pagar
    btn_pagar = tk.Button(janela, text="Pagar", command=pagar)
    btn_pagar.pack(pady=10)

    # Manter janela ativa
    janela.mainloop()

if __name__ == "__main__":
    main()
