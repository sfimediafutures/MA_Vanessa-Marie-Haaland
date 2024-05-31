class Threshold_filter:
    """
    A class that performs threshold filtering on a given DataFrame.

    Methods:
    - user_total_clicks: Filters the DataFrame based on the number of unique ads clicked (and not clicked) by each user.
    - items_total_clicks: Filters the DataFrame based on the number of unique users who clicked on each ad.
    - both_total_clicks: Iteratively runs both methods above until convergence.
    """

    def __init__(self) -> None:
        pass
    
    def user_total_clicks(self, df, threshold):
        # Calculate the unique ad counts for pos and neg df
        ad_counts_pos = df[df["click"] > 0].groupby("user_id")["item_id"].nunique()
        ad_counts_neg = df[df["click"] == 0].groupby("user_id")["item_id"].nunique()

        # filter by threshold
        ad_counts_pos = ad_counts_pos[ad_counts_pos >= threshold].reset_index(name='ad_count_click')
        ad_counts_neg = ad_counts_neg[ad_counts_neg >= threshold].reset_index(name='ad_count_non_click')

        # find common users (This assures that each user has both clicked on at least 3 different ads and seen 3 different ads without clicking)
        common_users_df = ad_counts_pos.merge(ad_counts_neg, on='user_id')

        # return list of common users
        valid_users = common_users_df['user_id'].tolist()
        df_valid_users = df[df["user_id"].isin(valid_users)].copy()

        return df_valid_users
    


    def items_total_clicks(self,df,threshold):
        df_pos = df[df["click"] > 0] #Only rows where a click is present

        users_per_ad = df_pos.groupby(["item_id"]).agg({"user_id":"nunique"}).reset_index()
        users_per_ad.columns = ["item_id", "num_users"]
        
        # Adding all ads with a click count over 3 to a list and creating a filtered dataframe
        temp = users_per_ad[users_per_ad["num_users"] >= threshold]
        valid_ads = set(temp["item_id"])
        df_valid_ads = df[df["item_id"].isin(valid_ads)].copy()

        return df_valid_ads
    
    def both_total_clicks(self, df, thresh_u, thresh_i):
        """
        Args:
            df (DataFrame): The input DataFrame containing user and item information.
            thresh_u (int): The minimum number of unique items clicked per user.
            thresh_i (int): The minimum number of unique users that clicked per item.
            
        Returns:
            DataFrame: The filtered DataFrame containing only rows where the number of clicks per user and per item
                       meet the specified thresholds.
        """
        df_pos = df[df["click"] > 0] #Only rows where a click is present
        
        while (min(df_pos["user_id"].value_counts()) < thresh_u) or (min(df_pos["item_id"].value_counts()) < thresh_i):
            df_user = self.user_total_clicks(df, thresh_u)
            df_pos = self.items_total_clicks(df_user, thresh_i)
            
        return df_pos