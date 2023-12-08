import metrics
import pandas as pd
import prediction_rank
import os
import sys
sys.path.append("../")
import config

ALL_METHODS = config.ALL_METHODS

def print(method =ALL_METHODS):
    sim_gt = pd.read_csv("similarity_based_gt.csv")
    rand_gt = pd.read_csv("random_based_gt.csv")
    for i in os.listdir("./predictions/similarity"):
        
        for m in method:
            subdir_path = os.path.join("./predictions/similarity", m, "prediction.csv")
            pred_df = pd.read_csv(subdir_path)
            metrics.main_metric(prediction_df=pred_df, gt_df= sim_gt)
            
            
print()