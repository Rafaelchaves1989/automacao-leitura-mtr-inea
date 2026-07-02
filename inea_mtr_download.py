import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import os

print("Automação do site INEA iniciada...")

# Caminhos configurados por Rafaela
caminho_planilha = r"C:\AutomacaoINEA\AutomacaoINEAplanilhasS.xlsx"
pasta_pdfs = r"C:\AutomacaoINEA\AutomacaoINEApdfs"

# Verifica se a pasta existe
os.makedirs(pasta_pdfs, exist_ok=True)

# Lê a planilha
df = pd.read_excel(caminho_planilha)

# A coluna com os MTRs deve se chamar "MTR N°"
lista_mtrs = df["MTR N°"].dropna().tolist()

print(f"Foram encontrados {len(lista_mtrs)} MTRs para processar.")

# Configura o Edge (modo visível)
options = Options()
options.add_experimental_option("detach", True)

service = Service()  # usa o EdgeDriver instalado no sistema
driver = webdriver.Edge(service=service, options=options)

# Assume que você já está logada manualmente no site
input("Por favor, entre manualmente no site do INEA e vá até 'Meus MTRs'. Depois pressione ENTER aqui para continuar...")

for mtr in lista_mtrs:
    try:
        print(f"Pesquisando MTR: {mtr}")

        # Localiza o campo "Número Manifesto" e preenche
        campo_mtr = driver.find_element(By.ID, "txtNumeroManifesto")
        campo_mtr.clear()
        campo_mtr.send_keys(str(mtr))
        time.sleep(1)

        # Clica em "Pesquisar"
        botao_pesquisar = driver.find_element(By.ID, "btnPesquisaMTR")
        botao_pesquisar.click()
        time.sleep(3)

        # Clica no botão "Visualizar MTR" (ícone PDF)
        botao_pdf = driver.find_element(By.XPATH, "//img[@title='Visualizar MTR']")
        botao_pdf.click()

        print(f"⏬ Baixando PDF do MTR {mtr}...")
        time.sleep(5)  # tempo para download concluir

    except Exception as e:
        print(f"⚠️ Erro ao processar o MTR {mtr}: {e}")

print("✅ Processo concluído! Todos os MTRs foram processados.")
driver.quit()
