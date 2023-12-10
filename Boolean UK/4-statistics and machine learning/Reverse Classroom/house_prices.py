import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

houses = pd.read_csv('houses_Madrid.csv')


df_houses=houses[['sq_mt_built','n_bathrooms','buy_price']]

df_houses=df_houses.dropna()

df_houses["sq_mt_built"]=df_houses["sq_mt_built"]/max(df_houses["sq_mt_built"])
df_houses["buy_price"]=df_houses["buy_price"]/max(df_houses["buy_price"])

colnames = list(["sq_mt_built","buy_price"])

conditions = [
    (df_houses['n_bathrooms'] <= 4),
    (df_houses['n_bathrooms'] > 4) & (df_houses['n_bathrooms'] <= 9),
    (df_houses['n_bathrooms'] > 9) & (df_houses['n_bathrooms'] <= 14),
    (df_houses['n_bathrooms'] > 14)
    ]

values = [1, 2, 3, 4]

df_houses['n_bath_class'] = np.select(conditions, values)

df_houses=df_houses.drop(columns=["n_bathrooms"])

print(df_houses.head())

customcmap = ListedColormap(["crimson", "mediumblue", "darkmagenta","blue"])


fig, ax = plt.subplots(figsize=(8, 6))
plt.scatter(x=df_houses['sq_mt_built'], y=df_houses['buy_price'], s=150,
            c=df_houses['n_bath_class'].astype('category'), 
            cmap = customcmap)
ax.set_xlabel(r'sq_mt_built', fontsize=14)
ax.set_ylabel(r'buy_price', fontsize=14)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
#plt.show()

#Functions:
def initiate_centroids(k, dset):
    '''
    Select k data points as centroids
    k: number of centroids
    dset: pandas dataframe
    '''
    centroids = dset.sample(k)
    return centroids

def rsserr(a,b):
    '''
    Calculate the root of sum of squared errors. 
    a and b are numpy arrays
    '''
    return np.square(np.sum((a-b)**2))

def centroid_assignation(dset, centroids):
    '''
    Given a dataframe `dset` and a set of `centroids`, we assign each
    data point in `dset` to a centroid. 
    - dset - pandas dataframe with observations
    - centroids - pa das dataframe with centroids
    '''
    k = centroids.shape[0]
    n = dset.shape[0]
    assignation = []
    assign_errors = []

    for obs in range(n):
        # Estimate error
        all_errors = np.array([])
        for centroid in range(k):
            err = rsserr(centroids.iloc[centroid, :], dset.iloc[obs,:])
            all_errors = np.append(all_errors, err)

        # Get the nearest centroid and the error
        nearest_centroid =  np.where(all_errors==np.amin(all_errors))[0].tolist()[0]
        nearest_centroid_error = np.amin(all_errors)

        # Add values to corresponding lists
        assignation.append(nearest_centroid)
        assign_errors.append(nearest_centroid_error)

    return assignation, assign_errors

def kmeans(dset, k=2, tol=1e-4):
    '''
    K-means implementationd for a 
    `dset`:  DataFrame with observations
    `k`: number of clusters, default k=2
    `tol`: tolerance=1E-4
    '''
    # Let us work in a copy, so we don't mess the original
    working_dset = dset.copy()
    # We define some variables to hold the error, the 
    # stopping signal and a counter for the iterations
    err = []
    goahead = True
    j = 0
    
    # Step 2: Initiate clusters by defining centroids 
    centroids = initiate_centroids(k, dset)

    while(goahead):
        # Step 3 and 4 - Assign centroids and calculate error
        working_dset['centroid'], j_err = centroid_assignation(working_dset, centroids) 
        err.append(sum(j_err))
        
        # Step 5 - Update centroid position
        centroids = working_dset.groupby('centroid').agg('mean').reset_index(drop = True)

        # Step 6 - Restart the iteration
        if j>0:
            # Is the error less than a tolerance (1E-4)
            if err[j-1]-err[j]<=tol:
                goahead = False
        j+=1

    working_dset['centroid'], j_err = centroid_assignation(working_dset, centroids)
    centroids = working_dset.groupby('centroid').agg('mean').reset_index(drop = True)
    return working_dset['centroid'], j_err, centroids

# Steps 1 and 2 - Define k and initiate the centroids
np.random.seed(42)
k=3
df=df_houses[['sq_mt_built','buy_price']]
centroids = initiate_centroids(k, df)
print(centroids)

# Step 3 - Calculate distance
for i, centroid in enumerate(range(centroids.shape[0])):
    err = rsserr(centroids.iloc[centroid,:], df.iloc[36,:])
    print('Error for centroid {0}: {1:.2f}'.format(i, err))

# Step 4 - Assign centroids
df['centroid'], df['error'] = centroid_assignation(df, centroids)
print(df.head())

fig, ax = plt.subplots(figsize=(8, 6))
plt.scatter(df.iloc[:,0], df.iloc[:,1],  marker = 'o', 
            c=df['centroid'].astype('category'), 
            cmap = customcmap, s=80, alpha=0.5)
plt.scatter(centroids.iloc[:,0], centroids.iloc[:,1],  
            marker = 's', s=200, c=[0, 1, 2], 
            cmap = customcmap)
ax.set_xlabel(r'sq_mt_built', fontsize=14)
ax.set_ylabel(r'buy_price', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()

print("The total error is {0:.2f}".format(df['error'].sum()))

# Step 5 - Update centroid location

centroids = df.groupby('centroid').agg('mean').loc[:, colnames].reset_index(drop = True)

fig, ax = plt.subplots(figsize=(8, 6))
plt.scatter(df.iloc[:,0], df.iloc[:,1],  marker = 'o', 
            c=df['centroid'].astype('category'), 
            cmap = customcmap, s=80, alpha=0.5)
plt.scatter(centroids.iloc[:,0], centroids.iloc[:,1],  
            marker = 's', s=200,
            c=[0, 1, 2], cmap = customcmap)
ax.set_xlabel(r'sq_mt_built', fontsize=14)
ax.set_ylabel(r'buy_price', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()

# Step 6 - Repeat steps 3-5
np.random.seed(42)
df['centroid'], df['error'], centroids =  kmeans(df[["sq_mt_built","buy_price"]], 3)
df.head()
print(centroids)

fig, ax = plt.subplots(figsize=(8, 6))
plt.scatter(df.iloc[:,0], df.iloc[:,1],  marker = 'o', 
            c=df['centroid'].astype('category'), 
            cmap = customcmap, s=80, alpha=0.5)
plt.scatter(centroids.iloc[:,0], centroids.iloc[:,1],  
            marker = 's', s=200, c=[0, 1, 2], 
            cmap = customcmap)
ax.set_xlabel(r'sq_mt_built', fontsize=14)
ax.set_ylabel(r'buy_price', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()

err_total = []
n = 10

df_elbow = df_houses[["sq_mt_built","buy_price"]]

for i in range(n):
    _, my_errs, _ = kmeans(df_elbow, i+1)
    err_total.append(sum(my_errs))
fig, ax = plt.subplots(figsize=(8, 6))
plt.plot(range(1,n+1), err_total, linewidth=3, marker='o')
ax.set_xlabel(r'Number of clusters', fontsize=14)
ax.set_ylabel(r'Total error', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()