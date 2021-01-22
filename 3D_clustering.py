from sklearn.cluster import KMeans
import pandas as pd

# Import csv file with data in following columns:
#    [PM (index)] [Longitude] [Latitude] [DaysUntilDueDate]

df = pd.read_csv('C:/Users/liche/Desktop/Path planning/TM_P3_F6/TM_P3_F6.csv',index_col=['no'])

K = 13

print("K-clusters: ", K)

for k in range(1,K):
    # Create a kmeans model on our data, using k clusters.
    #   Random_state helps ensure that the algorithm returns the
    #   same results each time.
    kmeans_model = KMeans(n_clusters=k, random_state=1).fit(df.iloc[:, :])

    # These are our fitted labels for clusters --
    #   the first cluster has label 0, and the second has label 1.
    labels = kmeans_model.labels_

    # Sum of distances of samples to their closest cluster center
    SSE = kmeans_model.inertia_

print("k:",k, " SSE:", SSE)

# Add labels to df
df['Labels'] = labels
print(df)

U_labels = df.Labels.unique()

alt_l = []
for j in labels:
    alt = df.loc[df['Labels'].eq(j),'z'].mean()
    alt_l.append(alt)

df['Mean'] = alt_l

U_alt=list(set(alt_l))
U_alt.sort()

label_id = 0
for l in U_alt:
    df.loc[df['Mean'] == l, ['Labels']] = label_id
    label_id += 1              

del df['Mean']

print(df)
df.to_csv('test_KMeans_out.csv')