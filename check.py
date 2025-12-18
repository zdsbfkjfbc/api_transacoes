import os

print("--- INVESTIGAÇÃO DE ARQUIVOS ---")
if os.path.exists("src"):
    print("Pasta 'src' encontrada.")
    arquivos = os.listdir("src")
    print(f"Arquivos dentro de src: {arquivos}")
    
    if "schemas.py" in arquivos:
        print("✅ O arquivo schemas.py ESTÁ LÁ!")
    elif "schemas.py.txt" in arquivos:
        print("❌ ERRO CRÍTICO: O arquivo é um .txt (schemas.py.txt)!")
    else:
        print("❌ ERRO: O arquivo schemas.py NÃO existe nesta pasta.")
else:
    print("❌ ERRO: A pasta 'src' não foi encontrada na raiz.")