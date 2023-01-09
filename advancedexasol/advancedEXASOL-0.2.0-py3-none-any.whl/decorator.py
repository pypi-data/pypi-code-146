import re
import pandas as pd


def ensure_table_exists(func):
    def wrapper(*args, **kwargs):
        # Get the AdvancedExaFeatures instance
        advanced_exa_features = args[0]
        source = args[1]
        target_table = args[2]

        # Check if the target table exists
        if not advanced_exa_features.table_exists(target_table):
            # Check if the source is a DataFrame
            if isinstance(source, pd.DataFrame):
                # Create the table from the DataFrame
                advanced_exa_features.create_table_from_df(target_table, source)
            elif isinstance(source, dd.DataFrame):
                # Create the table from the DataFrame
                advanced_exa_features.create_table_from_df(target_table, source.compute())
            else:
                # Create the table from the source table
                advanced_exa_features.create_table_from_table(target_table, source)
        else:
            # Get the column names for the target and source tables
            target_columns = advanced_exa_features.get_column_names(target_table)
            source_columns = advanced_exa_features.get_column_names(source)

            # Get the common columns between the target and source tables
            common_columns = list(set(target_columns) & set(source_columns))

            # Check if there are any missing columns in the target table
            if isinstance(source, pd.DataFrame) or isinstance(source, dd.DataFrame):
                missing_columns = [[col, advanced_exa_features.get_column_data_type_from_df(source, col)] for col in
                                   source_columns if col not in target_columns]
            else:
                missing_columns = [[col, advanced_exa_features.get_column_data_type(source, col)] for col in
                                   source_columns if col not in target_columns]

            if missing_columns:
                # Add the missing columns to the target table
                advanced_exa_features.add_columns(target_table, missing_columns)
            else:
                # Call the original function
                return func(*args, **kwargs)

    return wrapper

def ensure_connection(func):
    def wrapper(*args, **kwargs):
        # Get the AdvancedExaFeatures instance
        advanced_exa_features = args[0]

        # Check if the connection is closed
        if advanced_exa_features.conn.is_closed:
            # Re-establish the connection
            advanced_exa_features.conn = advanced_exa_features.connect(advanced_exa_features.connection_params)

        # Call the decorated function
        return func(*args, **kwargs)

    return wrapper

def handle_transactions(func):
    def wrapper(*args, **kwargs):
        # Get the AdvancedExaFeatures instance
        advanced_exa_features = args[0]

        # Start a transaction
        advanced_exa_features.cursor.execute("START TRANSACTION")

        try:
            # Call the original function
            result = func(*args, **kwargs)

            # Commit the transaction
            advanced_exa_features.cursor.execute("COMMIT")
        except Exception:
            # Rollback the transaction in case of an error
            advanced_exa_features.cursor.execute("ROLLBACK")
            raise

        return result

    return wrapper

def sql_injection_safe(func):
    def wrapper(*args, **kwargs):
        # Get the AdvancedExaFeatures instance
        advanced_exa_features = args[0]

        # Check all SQL queries passed to the decorated function
        for query in kwargs.values():
            # Check if the query contains any potentially dangerous characters
            if re.search(r'[^\w\s]', query):
                # Raise an exception if dangerous characters are found
                raise ValueError(
                    "SQL query contains potentially dangerous characters and may be vulnerable to injection attacks")

        # If no dangerous characters are found, execute the decorated function
        return func(*args, **kwargs)

    return wrapper

def enforce_resource_limits(func):
    def wrapper(*args, **kwargs):
        # Get the AdvancedExaFeatures instance
        advanced_exa_features = args[0]

        # Set the resource limits for the cursor
        advanced_exa_features.cursor.execute("SET MAX_CPU_OPERATION_TIME = 60")
        advanced_exa_features.cursor.execute("SET MAX_MEMORY_USAGE = 100000000")

        # Call the original function
        return func(*args, **kwargs)

    return wrapper