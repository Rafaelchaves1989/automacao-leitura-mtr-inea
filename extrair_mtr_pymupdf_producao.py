import pandas as pd
import re
import time

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =====================================
# CONFIGURAÇÕES
# =====================================
ARQUIVO_EXCEL = r"C:\meu_projeto_geo\planilha para puxar e-mail atraves do enpj.xlsx"
URL = "https://receitaws.com.br/"  # apenas o site foi alterado

# =====================================
# LER PLANILHA
# =====================================
print("🔹 Lendo planilha...")
df = pd.read_excel(ARQUIVO_EXCEL)

# Garante coluna de email
if len(df.columns) == 1:
    df["Email"] = ""

# =====================================
# EDGE
# =====================================
edge_options = Options()
edge_options.add_argument("--start-maximized")

driver = webdriver.Edge(service=Service(), options=edge_options)
wait = WebDriverWait(driver, 20)

# =====================================
# LOOP PRINCIPAL
# =====================================
for i, valor in enumerate(df.iloc[:, 0]):
    cnpj = re.sub(r"\D", "", str(valor))

    if len(cnpj) != 14:
        print(f"{i+1} ❌ CNPJ inválido")
        continue

    print(f"{i+1} 🔎 Consultando {cnpj}")
    driver.get(URL)

    # Campo de busca (MESMO SELETOR)
    campo = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//input[contains(@class,'input-search__input')]"
        ))
    )
    campo.clear()
    campo.send_keys(cnpj)

    # Botão Consultar Grátis (MESMO SELETOR)
    botao = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//span[contains(text(),'Consultar Grátis')]"
        ))
    )
    botao.click()

    time.sleep(3)

    # Buscar email dentro do <td> (MESMO SELETOR)
    try:
        email = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//td[contains(text(),'@')]"
            ))
        ).text.strip()
    except:
        email = "NÃO ENCONTRADO"

    # Grava resultado
    df.at[i, df.columns[1]] = email
    df.to_excel(ARQUIVO_EXCEL, index=False)

    # Fechar modal (MESMO SELETOR)
    try:
        fechar = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//i[contains(@class,'fa-times')]"
            ))
        )
        fechar.click()
        time.sleep(1)
    except:
        pass

# =====================================
# FINALIZA
# =====================================
driver.quit()
print("✅ Finalizado com sucesso")
