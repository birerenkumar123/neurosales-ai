import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def get_preprocessor():
    numeric_features = ['age', 'quantity', 'price']
    categorical_features = ['gender', 'category', 'payment_method', 'shopping_mall']

    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough'
    )
    return preprocessor

def feature_engineering(df):
    df_out = df.copy()
    
    # Create target column if possible
    if 'quantity' in df_out.columns and 'price' in df_out.columns:
        df_out['revenue'] = df_out['quantity'] * df_out['price']
        
    if 'invoice_date' in df_out.columns:
        # Convert date safely
        df_out['invoice_date'] = pd.to_datetime(df_out['invoice_date'], format="mixed", dayfirst=True)
        df_out['month'] = df_out['invoice_date'].dt.month
        df_out = df_out.drop(columns=['invoice_date'])
        
    # Drop unused/ID columns
    cols_to_drop = [c for c in ['invoice_no', 'customer_id'] if c in df_out.columns]
    if cols_to_drop:
        df_out = df_out.drop(columns=cols_to_drop)

    return df_out
