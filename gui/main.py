import tkinter as tk

def main():
    # Criar janela principal
    janela = tk.Tk()
    janela.title("Sistema de Caixa - Joalheria")
    janela.geometry("600x400")

    # Lista de venda (armazenar produtos adicionados)
    venda = []

    # Label de instrução
    label_codigo = tk.Label(janela, text="Digite o código do produto:")
    label_codigo.pack(pady=5)

    # Campo de entrada
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack(pady=5)

    # Área de resumo (produtos e total)
    resumo = tk.Text(janela, height=10, width=50)
    resumo.pack(pady=10)

    # Função para adicionar produto
    def adicionar_produto():
        codigo = entry_codigo.get()

        # Validar se é número
        if not codigo.isdigit():
            resumo.insert(tk.END, "Código inválido, digite apenas números.\n")
            return

        # Aqui futuramente vamos buscar no dicionário de produtos
        # Por enquanto, simulação:
        resumo.insert(tk.END, f"Produto código {codigo} adicionado.\n")
        venda.append({"descricao": f"Produto {codigo}", "preco": 10.0})

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

    # Manter janela ativa
    janela.mainloop()

if __name__ == "__main__":
    main()
