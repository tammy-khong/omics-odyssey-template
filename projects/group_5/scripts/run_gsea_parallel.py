import os
import pandas as pd
import gseapy as gp
from concurrent.futures import ProcessPoolExecutor

def run_single_gsea(fname, dea_dir, out_base):
    cell_type = fname.replace("_vs_rest.csv", "")
    print(f"[START] {cell_type}")

    df = pd.read_csv(os.path.join(dea_dir, fname))
    rnk = df[['gene', 'logfoldchange']].dropna()
    rnk = rnk.rename(columns={'logfoldchange': 'score'})
    rnk = rnk.drop_duplicates(subset=['gene']).sort_values('score', ascending=False)

    rnk_path = os.path.join(out_base, f"{cell_type}.rnk")
    rnk.to_csv(rnk_path, sep='\t', index=False, header=False)

    outdir_name = cell_type.replace(" ", "_").replace("(", "").replace(")", "")
    res = gp.prerank(
        rnk=rnk_path,
        gene_sets="GO_Biological_Process_2021",
        outdir=os.path.join(out_base, outdir_name),
        permutation_num=1000,
        min_size=15,
        max_size=500,
        seed=42,
        threads=2
    )

    print(f"[DONE] {cell_type}")
    return cell_type

def run_all_parallel():
    dea_dir = "gene_dea_results"
    out_base = "gsea_results"
    os.makedirs(out_base, exist_ok=True)

    files = [f for f in os.listdir(dea_dir) if f.endswith(".csv")]

    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(run_single_gsea, f, dea_dir, out_base)
            for f in files
        ]

        for fut in futures:
            try:
                fut.result()
            except Exception as e:
                print("[ERROR]", e)

if __name__ == "__main__":
    run_all_parallel()
