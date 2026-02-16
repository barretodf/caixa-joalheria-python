import tkinter as tk

def main():
    # Criar janela principal
    janela = tk.Tk()
    janela.title("Sistema de Caixa - Joalheria")
    janela.geometry("600x400")  # largura x altura

    # Label de instrução
    label_codigo = tk.Label(janela, text="Digite o código do produto:")
    label_codigo.pack(pady=5)

    # Campo de entrada
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack(pady=5)

    # Manter janela ativa
    janela.mainloop()

if __name__ == "__main__":
    main()
