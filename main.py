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
    # HISTÓRIA 6 (#7): VALIDAÇÕES BÁSICAS
    # ------------------
    venda = []  # lista para armazenar os itens escolhidos

    while True:
        codigo = input("\nDigite o código do produto (ou '0' para finalizar): ")

        # Impedir letras ou símbolos
        if not codigo.isdigit():
            print("Código inválido, digite apenas números positivos.")
            continue

        codigo = int(codigo)

        # Finalizar venda (tratar primeiro)
        if codigo == 0:
            if not venda:
                print("Nenhum produto foi adicionado. Encerrando o sistema.")
            break

        # Impedir valores negativos
        if codigo < 0:
            print("Código inválido, não pode ser negativo.")
            continue

        # Verificar se produto existe
        if codigo in produtos:
            produto = produtos[codigo]
            venda.append(produto)
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
