# ==================
# LEITURA DO CSV
# ==================

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
        print("Arquivo de produtos não encontrado.")
        return {}

    return produtos


# ==================
# INICIO DO SISTEMA
# ==================

def main():
    print("=== SISTEMA DE CAIXA - JOALHERIA ===")
    produtos = carregar_produtos("produtos.csv")

    if not produtos:
        print("Erro ao carregar produtos.")
        return

    print("\nProdutos disponíveis:")
    for codigo, dados in produtos.items():
        print(f"{codigo} - {dados['descricao']} (R$ {dados['preco']:.2f})")


if __name__ == "__main__":
    main()
