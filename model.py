import pandas as pd
from sklearn.neighbors import NearestNeighbors

class TreeRecommendation():
    def __init__(self):
        df_invtry_new = pd.read_csv('assets/data/combined_tree_data_with_header_with_derived_neighborhood.csv')

        # Drop ones without a condition score
        df_tree_cond = df_invtry_new.dropna(subset=['condition']).copy()

        # Convert case of all condition scores
        df_tree_cond.condition = df_tree_cond.condition.apply(lambda cond: cond.strip().lower())

        # Combine similar condition scores and ignore all others
        condition_map = {
            'excellent': 'good',
            'very good': 'good',
            'very': 'good',
            'good': 'good',
            'fair': 'fair',
            'poor': 'poor',
            'critial': 'poor',
        }
        df_tree_cond.condition = df_tree_cond.condition.map(condition_map)

        # Drop the trees that were not mapped
        df_tree_cond = df_tree_cond.dropna(subset=['condition'])

        # Convert to neg score for poor and positive for goodnp
        df_tree_cond['condition_score'] = df_tree_cond.condition.map({'good': 1, 'fair': 0, 'poor': -1})

        self.df_tree_cond = df_tree_cond

        # Create model and fit
        self.knn = NearestNeighbors(algorithm='ball_tree').fit(df_tree_cond[['latitude', 'longitude']])

    def data_html(self):
        return self.df_tree_cond.to_html()

    def recommend(self, latitude, longitude):
        print(latitude, longitude)

        # Get condition scores across the city
        dists, nearest_trees = self.knn.kneighbors(X=[[latitude, longitude]],
                                                   n_neighbors=25,
                                                   return_distance=True)

        # Keep recommendation spots that are close enough to existing trees
        mean_dist = dists[0].mean()
        if mean_dist > 0.005:
            return ['No-Result', 'Mean distance from nearest trees is {}.'.format(mean_dist)]

        nearest_trees = nearest_trees[0]
        df_pick = pd.DataFrame()
        local_trees = self.df_tree_cond.iloc[nearest_trees]
        df_pick['condition'] = local_trees.groupby(['scientific_species_name',
                                                    'common_species_name']).mean().condition_score
        df_pick['count'] = local_trees.groupby(['scientific_species_name',
                                                    'common_species_name']).count().condition_score

        pick = df_pick.sort_values(['condition', 'count'], ascending=False)

        return pick.reset_index()['common_species_name'].tolist()
