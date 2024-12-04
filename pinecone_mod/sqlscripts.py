

##static methods containing all the SQL scripts

def create_table_script(table_name):
    return f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                professor_name TEXT,
                classes TEXT,
                comments TEXT,
                difficulty TEXT,
                quality TEXT
            )
        """
def insert_data_script(table_name, professor_name, classes, comments, difficulty, quality):
    return f"""
    INSERT INTO {table_name} (professor_name, classes, comments, difficulty, quality)
    VALUES (?, ?, ?, ?, ?)
    """

def select_data(table_name):
    return f"""
            SELECT COUNT(*) FROM {table_name}
        """
