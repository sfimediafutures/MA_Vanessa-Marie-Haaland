import math
from sklearn.metrics import roc_auc_score

class Evaluation_Metrics():
    
    def __init__(self) -> None:
        pass
        
    
    def mean_average_precision(self, actual, recommended):
        if len(actual) != len(recommended):
            raise ValueError("Length of actual and predicted lists must be the same.")

        mean_ap = 0.0
        num_users = len(actual)
        tot_users = 0

        for i in range(num_users):
            ap = 0.0  # Average Precision for current user

            if len(actual[i]) == 0:
                continue
            tot_users += 1

            num_correct_predictions = 0
            precision_at_k = 0.0

            for j in range(len(recommended[i])):
                if recommended[i][j] in actual[i]:
                    num_correct_predictions += 1
                    precision_at_k += num_correct_predictions / (j + 1)

            if num_correct_predictions > 0:
                ap = precision_at_k / min(len(actual[i]), len(recommended[i]))

            mean_ap += ap

        mean_ap /= tot_users

        return mean_ap
    
    
    def precision_recall(self,actual, recommended):
        total_precision = 0
        total_recall = 0

        for idx in range(len(recommended)):
            tp=0
            fp=0
            recs = recommended[idx]
            targets = actual[idx]
            
            for item in recs:
                if item in targets:
                    tp+=1
                    
                else:
                    fp+=1
            fn = len(targets) - tp
            
            total_precision += tp / (tp + fp)
            total_recall += tp / (tp + fn)
        
        return total_precision/len(recommended), total_recall/len(recommended)
    
    
    def ndcg(self,actual, recommended):
        gains = []
        for idx in range(len(recommended)):
            liked_set = set(actual[idx])
            rec_items = recommended[idx]
            user_gains = [1 if item in liked_set else 0 for item in rec_items]
            gains.append(user_gains)
        
        dcg = 0
        for user in gains:
            for idx in range(len(user)):
                rank = idx + 1
                gain = user[idx]
                x = math.log2(rank + 1)
                dcg += gain/x

        idcg = 0
        ideal = []
        for user in range(len(actual)):
            temp_ideal = []
            for item in actual[user]:
                temp_ideal.append(1)
            if len(temp_ideal) > len(recommended[user]):
                missing = len(temp_ideal) - len(recommended[user])
                temp_ideal.extend([0]*missing)
            ideal.append(temp_ideal)
        for user in ideal:
            for idx in range(len(user)):
                rank = idx + 1
                gain = user[idx]
                x = math.log2(rank + 1)
                idcg += gain/x
        
        ndcg = dcg/idcg
        return ndcg

    