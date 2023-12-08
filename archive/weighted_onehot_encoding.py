import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import re


def extract_feature_name(col_name):
    match = re.search(r'^(.*?)(?:_\d+)?$', col_name)
    return match.group(1)+"_confidence" if match else col_name


def weighted_onehot_encoder(df, categorical):
    """one hot encode the data so that confidence is built in as a score for categorical variables
    
    If key is 0 and key_confidence is 0.56, then it will show up as key_0_confidence = 0.56, the other encoded values will be 0 (e.x. key_1_confidence = 0)
    Does not process any other columns.

    Args:
        df (pd.DataFrame): raw data minus identifiers!! (things like song name, track id needs to be excluded before passed in)
        categorical (list): list of column names that are categorical variables
        
    NOTE: make sure the confidence columns follow this format: "{CATEGORICALNAME}_confidence"
    """
    
    categorical_conf = [cat + "_confidence" for cat in categorical]
    numeric_columns = [num for num in df.columns if (num not in categorical) & (num not in categorical_conf) ]
    

    weight_matrix_numeric = pd.DataFrame(np.ones(df[numeric_columns].shape), columns=numeric_columns)

    cat = df[categorical]
    
    preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical)
    ],
    remainder='passthrough'  
)
    oh_cat = preprocessor.fit_transform(cat).toarray()
    oh_cat_col_names = list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical))

    oh_cat_df = pd.DataFrame(oh_cat, columns=oh_cat_col_names)
    weight_matrix_oh_conf = oh_cat_df.copy()
    for col_name in weight_matrix_oh_conf.columns:
        conf_col_name = extract_feature_name(col_name)
        nonzero_mask = weight_matrix_oh_conf[col_name] != 0

        weight_matrix_oh_conf[col_name][nonzero_mask] = df[conf_col_name][nonzero_mask]

    weight_matrix = pd.concat([weight_matrix_numeric, weight_matrix_oh_conf], axis=1)
    full_oh_df = pd.concat([df[numeric_columns], oh_cat_df], axis = 1)
    

    #assert weight_matrix_oh_conf.shape[0] == df.shape[0], "confidence data frame and original data frame does not have the same number of rows"
    assert weight_matrix.shape == full_oh_df.shape, "Your weight matrix and one hot encoded dataframe (with no confidence columns) do not share the same shape"
    weighted_full_oh_df = weight_matrix * full_oh_df
    # print(weight_matrix)
    # print(full_oh_df)
    return weighted_full_oh_df

if __name__=="__main__":
    df = pd.read_csv("h5_dataset.csv")
    features = df.drop(columns=["Unnamed: 0", "track_id", "formatted_data"])

    weighted_features = weighted_onehot_encoder(features, categorical = ["key", "mode", "time_signature"])
    weighted_features_with_names = pd.concat([df[["formatted_data", "track_id"]], weighted_features],axis=1)
    weighted_features_with_names.to_csv("weighted_features_with_names.csv",index=False)    
    

    
    
    
    
    
    
    