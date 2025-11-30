import pandas as pd

# --- 1. O CAMINHO DO ARQUIVO ---
# Coloque aqui o nome exato do arquivo que você baixou.
# Se estiver na mesma pasta do script, basta o nome.
# Se estiver em outra pasta, precisa do caminho completo (ex: "C:/Users/Downloads/sequence.fna")
filename = "archive/MN908947.fna"  # <--- ALTERE AQUI PARA O SEU ARQUIVO (.fna, .txt ou .fasta)

# --- 2. O ALGORITMO DE PARSING (Mantém igual) ---
def parse_fasta(file_path):
    sequences = []
    headers = []
    labels = []
    
    current_seq = []
    current_header = None
    
    print(f"Lendo arquivo: {file_path}...")
    
    # Adicionamos encoding='utf-8' para garantir
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue 
            
            if line.startswith(">"):
                if current_header:
                    full_seq = "".join(current_seq)
                    sequences.append(full_seq)
                    headers.append(current_header)
                    
                    # Lógica de classificação
                    header_lower = current_header.lower()
                    if "coronavirus 2" in header_lower or "covid" in header_lower or "sars-cov-2" in header_lower:
                        labels.append("COVID-19")
                    elif "sars coronavirus" in header_lower: # Cuidado para não confundir com sars-cov-2
                        labels.append("SARS")
                    elif "middle east" in header_lower or "mers" in header_lower:
                        labels.append("MERS")
                    else:
                        labels.append("OUTRO")
                
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
        
        # Salva o último
        if current_header:
            full_seq = "".join(current_seq)
            sequences.append(full_seq)
            headers.append(current_header)
            
            header_lower = current_header.lower()
            if "coronavirus 2" in header_lower or "covid" in header_lower or "sars-cov-2" in header_lower:
                labels.append("COVID-19")
            elif "sars coronavirus" in header_lower:
                labels.append("SARS")
            elif "middle east" in header_lower or "mers" in header_lower:
                labels.append("MERS")
            else:
                labels.append("OUTRO")
                
    return pd.DataFrame({
        'id': headers,
        'label': labels,
        'sequence': sequences
    })

# --- 3. EXECUTANDO ---
# Certifique-se de que o arquivo existe antes de rodar
try:
    df = parse_fasta(filename)
    print("Sucesso! Arquivo carregado.")
    print(df['label'].value_counts())
except FileNotFoundError:
    print(f"ERRO: Não encontrei o arquivo '{filename}'. Verifique se o nome está correto.")