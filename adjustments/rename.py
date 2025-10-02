from pathlib import Path
import pandas as pd

folder = Path(".")  # change this
mapping = {"z_boom_u": "z_boom_cor_u", "z_boom_l": "z_boom_cor_l", "z_stake": "z_stake_cor"}

for csv_path in folder.glob("*.csv"):
    df = pd.read_csv(csv_path)
    if "variable" in df.columns:
        df["variable"] = df["variable"].replace(mapping)
        df.to_csv(csv_path, index=False)
