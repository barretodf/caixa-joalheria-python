import tkinter as tk
import csv

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
    janela = tk.Tk()
    janela.title("Sistema de Caixa - Joalheria")
    janela.geometry("600x400")

    # Área para listar produtos disponíveis
    lista_produtos = tk.Text(janela, height=10, width=50)
    lista_produtos.pack(pady=10)

    def atualizar_lista():
        lista_produtos.delete("1.0", tk.END)
        produtos = carregar_produtos(ARQUIVO_PRODUTOS)
        lista_produtos.insert(tk.END, "Produtos disponíveis:\n")
        for codigo, dados in produtos.items():
            lista_produtos.insert(tk.END, f"{codigo} - {dados['descricao']} (R$ {dados['preco']:.2f})\n")

    atualizar_lista()  # carregar ao iniciar

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
                atualizar_lista()  # atualizar lista na tela principal
            else:
                tk.Label(cadastro, text="Dados inválidos.").pack(pady=5)

        tk.Button(cadastro, text="Salvar", command=salvar).pack(pady=10)

    # Botão principal para abrir cadastro
    btn_cadastrar = tk.Button(janela, text="Cadastrar produto", command=abrir_cadastro)
    btn_cadastrar.pack(pady=10)

    janela.mainloop()

if __name__ == "__main__":
    main()
