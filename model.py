import os
import pandas as pd
from sklearn.neighbors import NearestNeighbors

class TreeRecommendation():
    def __init__(self):
        print('*'*25)
        print('INITIALIZING MODEL')

        df_invtry_new = pd.read_csv('assets/data/trees.csv')
        # Drop ones without a condition score
        df_tree_cond = df_invtry_new.dropna(subset = ['condition']).copy()

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
        df_tree_cond = df_tree_cond.dropna(subset = ['condition'])

        # Convert to neg score for poor and positive for good tree conditions
        df_tree_cond['condition_score'] = df_tree_cond.condition.map({'good': 1, 'fair': 0, 'poor': -1})

        self.df_tree_cond = df_tree_cond

        # Create model and fit
        self.knn = NearestNeighbors(algorithm = 'ball_tree').fit(df_tree_cond[['latitude', 'longitude']])

        # Load the rules dataset
        df_rules = pd.read_excel('assets/data/sf_tree_rules.xlsx', sheetname = 0)
        self.allowed_species = pd.DataFrame(df_rules['species'].apply(lambda x: x.lower()))
        print('Allowed species:', ', '.join(self.allowed_species['species'].values))

    def data_html(self):
        return self.df_tree_cond.to_html()

    def recommend(self, latitude, longitude):
        print('Recommending for', latitude, 'lat', longitude, 'long')

        # Get condition scores across the city
        dists, nearest_trees = self.knn.kneighbors(X = [[latitude, longitude]],
                                                   n_neighbors = 25,
                                                   return_distance = True)

        # Keep recommendation spots that are close enough to existing trees
        mean_dist = dists[0].mean()
        if mean_dist > os.environ.get('MEAN_DISTANCE_CUTOFF', 0.01):
            return ['No-Result', 'Mean distance from nearest trees is {}.'.format(mean_dist)]

        # Select mean coundition of the nearby species
        nearest_trees = nearest_trees[0]
        df_pick = pd.DataFrame()
        local_trees = self.df_tree_cond.iloc[nearest_trees]
        df_pick['condition'] = local_trees.groupby(['botanical', 'common']).mean().condition_score
        df_pick['count'] = local_trees.groupby(['botanical', 'common']).count().condition_score

        pick = df_pick.sort(['condition', 'count'],
                            ascending = False).reset_index()

        pick['botanical'] = pick['botanical'].apply(lambda x: x.lower())

        # Filter down to allowed species
        joined = pd.merge(pick, self.allowed_species,
                          left_on = 'botanical', right_on = 'species', how = 'inner')

        if len(joined) == 0:
            return ['No-Result', 'Nearby trees are not allowed to be planted.']

        return joined['common'].apply(lambda x: x.lower()).tolist()

