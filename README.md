# MA_Vanessa-Marie-Haaland

Title: Personalized Advertisement Recommendations Using Implicit Feedback

Supervisor: Assoc. Prof. Dr. Mehdi Elahi

Co-supervisor: Vice President of AI, Dr. Igor Pipkin

This work was supported by industry partners and the Research Council of Norway with funding to MediaFutures: Research Centre for Responsible Media Technology and Innovation, through The Centers for Research-based Innovation scheme, project number 309339.


### Threshold_Filtering.py
The class in this files is used to remove all users that had clicked on less than 3 different ads, and all ads that had been clicked by less than 10 different users

### Scoring_Approaches.py
Contains a class to add each of the different proposed approaches for inferring user-item preferences

### Baseline_recommenders.py
Contains two classes, one for each of the baseline models used in the offline evaluation.

### Evaluation_Metrics.py
Contains a class with methods for the performance metrics used during the offline evaluation; Precision, Recall, MAP and NDCG.

### Offline_Eval.ipynb
A Jupyter Notbook with all the code for the offline evaluation. Imports all the other files in this repo.
