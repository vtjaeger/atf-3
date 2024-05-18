import requests # type: ignore
import openpyxl # type: ignore

def buscar_repositorios():
    url = 'https://api.github.com/repositories'
    resposta = requests.get(url)
    resposta.raise_for_status()  # caso erro
    return resposta.json()

def contar_repositorios(repositorios):
    qtd_com_json = 0
    qtd_sem_json = 0

    for repo in repositorios:
        descricao = repo.get('description', '')
        if descricao and isinstance(descricao, str) and 'json' in descricao.lower():
            qtd_com_json += 1
        else:
            qtd_sem_json += 1

    return qtd_com_json, qtd_sem_json

def criar_excel(qtd_com_json, qtd_sem_json):
    workbook = openpyxl.Workbook()
    planilha = workbook.active

    planilha.append(["Contem JSON", "Repositorios"])
    planilha.append(["Sim", qtd_com_json])
    planilha.append(["Nao", qtd_sem_json])

    workbook.save("output.xlsx")

def main():
    try:
        repositorios = buscar_repositorios()
        qtd_com_json, qtd_sem_json = contar_repositorios(repositorios)
        criar_excel(qtd_com_json, qtd_sem_json)
        print("excel salvo")
    except requests.exceptions.RequestException as e:
        print(f"erro: {e}")
    except Exception as e:
        print(f"erro 2:  {e}")

if __name__ == "__main__":
    main()
