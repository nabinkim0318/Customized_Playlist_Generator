# Function to load data
def load_music_data(data_path):
    data = pd.read_csv(data_path)
    return data


# Function for K-Means Clustering
def kmeans_clustering(data, user_selected_songs_features):
    num_clusters = len(user_selected_songs_features)
    kmeans = KMeans(n_clusters=num_clusters, init=np.array(user_selected_songs_features), n_init=1, random_state=42)
    data['kmeans_cluster'] = kmeans.fit_predict(data)
    return data


# Function for Gaussian Mixture Model (GMM) Clustering
def gmm_clustering(data, user_selected_songs_features):
    num_clusters = len(user_selected_songs_features)
    gmm = GaussianMixture(n_components=num_clusters, init_params='kmeans', random_state=42)
    gmm.means_init = np.array(user_selected_songs_features)
    data['gmm_cluster'] = gmm.fit_predict(data)
    return data


# Function for DBSCAN Clustering
def dbscan_clustering(data, eps_values, min_samples_values):
    best_eps = None
    best_min_samples = None
    best_silhouette_score = -1

    for eps in eps_values:
        for min_samples in min_samples_values:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            clusters = dbscan.fit_predict(data)
            if len(set(clusters)) > 1:  # Ensure more than one cluster is formed
                silhouette_avg = silhouette_score(data, clusters)
                if silhouette_avg > best_silhouette_score:
                    best_silhouette_score = silhouette_avg
                    best_eps = eps
                    best_min_samples = min_samples

    return best_eps, best_min_samples



if __name__ == "__main__":
    # Load music data
    data = load_music_data(df)

    # Collect user-selected songs' features
    user_selected_songs_features = [
        [0.6, 0.7, ...],  # Feature vector of song 1
        [0.8, 0.6, ...],  # Feature vector of song 2
        # Add more user-selected songs as needed
    ]

    # Perform K-Means Clustering
    data = kmeans_clustering(data, user_selected_songs_features)

    # Perform GMM Clustering
    data = gmm_clustering(data, user_selected_songs_features)

    # Define range of hyperparameters for DBSCAN
    eps_values = [0.1, 0.2, 0.3, 0.4, 0.5]
    min_samples_values = [5, 10, 15, 20]

    # Perform DBSCAN Clustering and find the best parameters
    best_eps, best_min_samples = dbscan_clustering(data, eps_values, min_samples_values)

    print(f"Best Parameters - eps: {best_eps}, min_samples: {best_min_samples}")

    # Visualize the clusters if needed
    for cluster_method in ['kmeans', 'gmm']:
        plt.figure(figsize=(8, 6))
        plt.scatter(data['danceability'], data['energy'], c=data[f'{cluster_method}_cluster'], cmap='viridis')
        plt.title(f'{cluster_method.capitalize()} Clustering')
        plt.xlabel('Danceability')
        plt.ylabel('Energy')
        plt.show()

