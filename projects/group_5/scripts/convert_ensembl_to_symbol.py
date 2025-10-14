import os
import pandas as pd
import mygene

# Input and output directories
input_dir = 'dea_results'
output_dir = 'gene_dea_results'
os.makedirs(output_dir, exist_ok=True)

# Initialize mygene client
mg = mygene.MyGeneInfo()

# List all CSV files
for filename in os.listdir(input_dir):
    if not filename.endswith(".csv"):
        continue

    # Load the DEA result
    path = os.path.join(input_dir, filename)
    df = pd.read_csv(path)

    # Query MyGene to map Ensembl IDs to gene symbols
    ensembl_ids = df['gene'].dropna().unique().tolist()
    result = mg.querymany(ensembl_ids, scopes='ensembl.gene', fields='symbol', species='mouse', as_dataframe=True)

    # Create mapping
    symbol_map = result['symbol'].to_dict()
    df['gene_symbol'] = df['gene'].map(symbol_map)

    # Drop genes that could not be mapped
    df = df.dropna(subset=['gene_symbol'])

    # Drop duplicates if any
    df = df.drop_duplicates(subset=['gene_symbol'])

    # Replace Ensembl with symbol
    df['gene'] = df['gene_symbol']
    df = df.drop(columns=['gene_symbol'])

    # Save to output dir
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")
