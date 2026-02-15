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
    # AJUSTE: DIGITAR CÓDIGO E MOSTRAR PRODUTO
    # ------------------
    venda = []  # lista para armazenar os itens escolhidos

    while True:
        codigo = input("\nDigite o código do produto (ou '0' para finalizar): ")

        # Valida se é numérico
        if not codigo.isdigit():
            print("Código inválido, digite apenas números.")
            continue

        codigo = int(codigo)

        # Permite sair digitando 0
        if codigo == 0:
            break

        # Verifica se produto existe
        if codigo in produtos:
            produto = produtos[codigo]
            venda.append(produto)  # adiciona à lista
            print(f"Produto: {produto['descricao']} - Preço: R$ {produto['preco']:.2f}")
        else:
            print("Produto não encontrado.")

    # ------------------
    # SOMA FINAL
    # ------------------
    print("\nResumo da venda:")
    total = 0
    for item in venda:
        print(f"- {item['descricao']} (R$ {item['preco']:.2f})")
        total += item['preco']

    print(f"Total da venda: R$ {total:.2f}")


if __name__ == "__main__":
    main()
