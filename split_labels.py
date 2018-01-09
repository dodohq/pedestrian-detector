# pylint: disable-all

import numpy as np
import pandas as pd
import math
np.random.seed(1)

full_labels = pd.read_csv('data/pedestrian_labels.csv')
print(full_labels.head())

grouped = full_labels.groupby('filename')
grouped.apply(lambda x: len(x)).value_counts()

grouped_list = [grouped.get_group(x) for x in grouped.groups]
print(len(grouped_list))

train_idx = np.random.choice(len(grouped_list), size=math.floor(
    len(grouped_list) * 0.8), replace=False)
test_idx = np.setdiff1d(list(range(len(grouped_list))), train_idx)

train = pd.concat([grouped_list[i] for i in train_idx])
test = pd.concat([grouped_list[i] for i in test_idx])

print((len(train), len(test)))

train.to_csv('data/train_labels.csv', index=None)
test.to_csv('data/test_labels.csv', index=None)
