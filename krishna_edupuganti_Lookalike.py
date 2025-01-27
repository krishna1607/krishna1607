# Filter transactions for the first 20 customers (C0001 to C0020)
selected_customers = full_data[full_data["CustomerID"].isin([f"C{str(i).zfill(4)}" for i in range(1, 21)])]
# Create customer profiles by aggregating transaction data
customer_profiles = selected_customers.groupby("CustomerID").agg({
    "TotalValue": "sum",  # Total spending
    "Quantity": "sum",    # Total quantity purchased
    "Category": lambda x: x.mode()[0] if not x.mode().empty else None,  # Most purchased category
    "Region": "first"     # Region (assumes no changes per customer)
}).reset_index()

# Rename columns for clarity
customer_profiles.rename(columns={
    "TotalValue": "TotalSpending",
    "Quantity": "TotalQuantity",
    "Category": "TopCategory",
}, inplace=True)

# Display customer profiles for inspection
customer_profiles.head()

from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# One-hot encode categorical features (TopCategory, Region)
encoder = OneHotEncoder()
categorical_features = encoder.fit_transform(customer_profiles[["TopCategory", "Region"]]).toarray()

# Scale numerical features (TotalSpending, TotalQuantity)
scaler = MinMaxScaler()
numerical_features = scaler.fit_transform(customer_profiles[["TotalSpending", "TotalQuantity"]])

# Combine numerical and categorical features into a single feature matrix
feature_matrix = pd.concat([
    pd.DataFrame(numerical_features, columns=["ScaledSpending", "ScaledQuantity"]),
    pd.DataFrame(categorical_features, columns=encoder.get_feature_names_out())
], axis=1).values

# Compute pairwise cosine similarity between customers
similarity_matrix = cosine_similarity(feature_matrix)

# Create a mapping of each customer to their top 3 similar customers
lookalike_map = {}
customer_ids = customer_profiles["CustomerID"].tolist()
for i, customer_id in enumerate(customer_ids):
    # Get similarity scores for the current customer
    scores = list(enumerate(similarity_matrix[i]))
    # Sort by score (descending) and exclude self-similarity
    top_similar = sorted(scores, key=lambda x: x[1], reverse=True)[1:4]
    # Map customer to their top 3 similar customers with scores
    lookalike_map[customer_id] = [(customer_ids[j], round(score, 4)) for j, score in top_similar]

# Display the lookalike map for inspection
lookalike_map


