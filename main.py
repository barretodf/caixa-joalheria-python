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

    # ------------------
    # LISTAR PRODUTOS
    # ------------------
    print("\nProdutos disponíveis:")
    for codigo, dados in produtos.items():
        print(f"{codigo} - {dados['descricao']} (R$ {dados['preco']:.2f})")

    # ------------------
    # HISTÓRIA 2 (#3): BUSCAR PRODUTO PELO CÓDIGO
    # ------------------
    # Solicita ao usuário um código de produto
    codigo = input("\nDigite o código do produto que deseja buscar: ")

    # Valida se a entrada é numérica
    if not codigo.isdigit():
        print("Código inválido, digite apenas números.")
        return

    codigo = int(codigo)

    # Verifica se o produto existe no dicionário
    if codigo in produtos:
        produto = produtos[codigo]
        print(f"Produto encontrado: {produto['descricao']} - Preço: R$ {produto['preco']:.2f}")
    else:
        print("Produto não encontrado.")


if __name__ == "__main__":
    main()
