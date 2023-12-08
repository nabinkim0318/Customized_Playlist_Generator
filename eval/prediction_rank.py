import pandas as pd
import os

def read_predictions(path):
    
    
    return pd.read_csv(path)

def create_folders_for_methods(df, high_level="similarity"):
    
    for i in df["Similarity_method"].unique():
        os.makedirs(f"./predictions/{high_level}/{i}", exist_ok=True)
        subpath = f"./predictions/{high_level}/{i}"
        pred_subdf = df.loc[df["Similarity_method"] == i, ["Seed_song_names", "All_songs"]]
        pred_subdf["Rank"] = [1,2,3,4,5] * 5
        pred_subdf.to_csv(f"{subpath}/prediction.csv", index=False)
    
    return


def main():
    
    sim_pred = read_predictions("similarity_based_luhee_top5.csv")
    create_folders_for_methods(sim_pred)
    random_pred = read_predictions("random_songs_luhee_top5.csv")
    create_folders_for_methods(random_pred, high_level="random")

main()
    