import os
import sys

arquivos = os.listdir("codigo/python")
print(arquivos)
exemplos = []
for arquivo in arquivos:
    if arquivo.endswith("_before.py"):
        conteudo = open(os.path.join("codigo", "python", arquivo), "r").read()
        exemplos.append(
            {
                "nome": arquivo[:-10].replace("-", " ").title(),
                "caminho": os.path.join("codigo", "python", arquivo),
                "conteudo": conteudo,
            }
        )


def main():
    print("Exemplos de código Python:")
    for exemplo in exemplos:
        print(f"- {exemplo['nome']}: {exemplo['caminho']} \n\n{exemplo['conteudo']}\n")
    if not os.path.exists("codigo/python-antes"):
        os.mkdir("codigo/python-antes")
    for i, exemplo in enumerate(exemplos):
        print(f"{i},{exemplo['nome']}")
        caminho_destino = os.path.join("codigo", "python-antes", str(i) + ".py")
        with open(caminho_destino, "w") as f:
            f.write(exemplo["conteudo"])


if __name__ == "__main__":
    main()
