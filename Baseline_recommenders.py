import random

class Popularity_recommender:
    def __init__(self):
        self.trainset = None
        self.popularity_df = None
    
    # The most popular ads are the ones most different users have clicked, not the ones with highest number of clicks.
    def fit(self, X_df):
        self.trainset = X_df.copy()
        pos_df = X_df[X_df['click']>0]
        result = (pos_df.groupby("item_id")["user_id"]
          .nunique()
          .reset_index(name="num_users")
          .sort_values("num_users", ascending=False))
        self.popularity_df = result

    def recommend(self, userid, matrix = None, N = 10, filter_already_liked_items = True):
        pop_df = self.popularity_df.copy()
        if filter_already_liked_items:
            existing_clicks = self.trainset[self.trainset["user_id"] == userid]["item_id"].to_list()
            pop_df = pop_df[~pop_df["item_id"].isin(existing_clicks)]
        
        total_users = self.trainset["user_id"].nunique()

        # The score is the ratio of users that have clicked each item. Not the ratio of all clicks, but of all users. 
        pop_df['score'] = (pop_df['num_users']/total_users).round(6)
        
        return pop_df["item_id"].head(N).tolist(), pop_df["score"].head(N).tolist()
      
        
class Random_recommender:
    def __init__(self) -> None:
        self.trainset = None
        
    def fit(self, X_df):
        self.trainset = X_df

    def recommend(self, userid, matrix=None, N=10, filter_already_liked_items = True):
        rand_df = self.trainset.copy()
        if filter_already_liked_items:
            existing_clicks = self.trainset[self.trainset["user_id"] == userid]["item_id"].to_list()
            rand_df = rand_df[~rand_df["item_id"].isin(existing_clicks)]
        
        unique_items = rand_df["item_id"].unique().tolist()

        random_recs = random.sample(unique_items, N)

        return random_recs, [0] * N        # Don't need scores when recommendations are random anyway