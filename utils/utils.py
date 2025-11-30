import pandas as pd
import matplotlib.pyplot as plt

def parse_fasta_optimized(file_path):
    ids = []
    sequences = []
    current_seq = []
    current_id = None
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith(">"):
                if current_id:
                    ids.append(current_id)
                    sequences.append("".join(current_seq))
                
                parts = line.split('|')
                if len(parts) >= 2:
                    current_id = parts[1]
                else:
                    current_id = line[1:] 
                
                current_seq = []
            else:
                current_seq.append(line)
        if current_id:
            ids.append(current_id)
            sequences.append("".join(current_seq))
            
    return pd.DataFrame({'id': ids, 'sequence': sequences})

nome_fasta = "archive/ALL-HUMAN-0001 SEQUENCES.fasta"
nome_txt = "archive/ALL-HUMAN-0001-ANNOTATIONS.txt"

print("Processando FASTA...")
df_seq = parse_fasta_optimized(nome_fasta)
print(f"Sequências carregadas: {len(df_seq)}")

print("Processando TXT (Anotações)...")

try:
    df_annot = pd.read_csv(nome_txt, sep=None, engine='python', header=None, names=['col_id_go', 'function', 'source'])
except:
    print("Aviso: Tentativa de leitura padrão falhou, tentando forçar separador...")
    df_annot = pd.read_csv(nome_txt, sep=r'\s+', engine='python', header=None, names=['col_id_go', 'function', 'source'])

df_annot['col_id_go'] = df_annot['col_id_go'].astype(str)
df_annot['function'] = df_annot['function'].astype(str)

df_annot['id'] = df_annot['col_id_go'].apply(lambda x: x.split()[0])

df_annot['function_clean'] = df_annot['function'].str.replace(r'^[FPC]:', '', regex=True).str.strip()

df_annot = df_annot[df_annot['function'].str.contains('F:', na=False)]

df_annot_unique = df_annot.drop_duplicates(subset='id', keep='first')

print(f"Anotações únicas (IDs): {len(df_annot_unique)}")

print("Cruzando dados (Merge)...")
df_final = pd.merge(df_seq, df_annot_unique[['id', 'function_clean']], on='id', how='inner')

print("\n" + "="*30)
print("DATASET FINAL PRONTO")
print("="*30)
print(df_final.head())
print(f"\nTamanho do Dataset: {len(df_final)} exemplos")

print("\nTop 10 Funções mais comuns (Nossas Classes):")
top_10_counts = df_final['function_clean'].value_counts().head(10)
print(top_10_counts)

df_final.to_csv("dataset_processado.csv", index=False)

plt.figure(figsize=(12, 6))
top_10_counts.plot(kind='bar', color='#4c72b0', edgecolor='black')
plt.title('Top 10 Funções de Proteínas Mais Comuns')
plt.xlabel('Função')
plt.ylabel('Número de Amostras')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('distribuicao_amostras.png')
plt.show()