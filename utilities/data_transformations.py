# convert yes or no column to trye or false
def yes_no_to_boolean(df, column):
    df[column] = df[column].str.lower()
    df[column] = df[column].replace({"yes": True, "no": False})
    return df