import metrics
import pandas as pd
import prediction_rank
import os
import sys
sys.path.append("../")
import config

ALL_METHODS = config.ALL_METHODS

def print_test(method =ALL_METHODS):
    sim_gt = pd.read_csv("similarity_based_gt.csv")
    rand_gt = pd.read_csv("random_based_gt.csv")
    # sim_gt["Seed_song_names"] = sim_gt["Seed_song_names"].str.strip()
    # sim_gt["All_songs"] = sim_gt["All_songs"].str.strip()

    for i in os.listdir("./predictions/similarity"):
        counter = 0
        for m in method:
            print(f"METHOD: {m}")
            if m == "vggish":
                subdir_path = os.path.join("./predictions/similarity", m, "prediction.csv")
            else:
                subdir_path = os.path.join("./eval/predictions/similarity", m, "prediction.csv")
            pred_df = pd.read_csv(subdir_path)
            # pred_df["Seed_song_names"] = pred_df["Seed_song_names"].str.strip()
            # pred_df["All_songs"] = pred_df["All_songs"].str.strip()
            metrics.main_metric(counter=counter, prediction_df=pred_df, gt_df= sim_gt)
            counter +=1
            
            
print_test()