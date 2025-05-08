def validate_data(data):
    # Simple check: no empty values
    return not data.isnull().values.any()
