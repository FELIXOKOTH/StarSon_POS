def validate_data(df):
    required_columns = ["name", "email", "role"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"[ERROR] Missing columns: {missing}")
        return False
    return True

