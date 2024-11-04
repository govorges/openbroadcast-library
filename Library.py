from Database import Database

class LibraryManager:
    def __init__(self) -> None:
        self.database = Database()

    def associate_library_with_googleid(self, library_id: str, google_id: str):
        user_data = self.retrieve_user_by_google_id(google_id=google_id)
        user_metadata = user_data[1]
        user_metadata['library'] = library_id
        
        sql_query = f"""
        UPDATE public."Users"
        SET account_metadata = %s
        WHERE google_id = %s;
        """
        self.database.execute_sql_query(sql_query, args=(user_metadata, google_id))
        

    def retrieve_user_by_google_id(self, google_id: str):
        sql_query = f"""
        SELECT google_id, account_metadata, date_created FROM public."Users" WHERE google_id = %s
        """
        cursor = self.database.execute_sql_query(sql_query, args=(google_id,))
        return cursor.fetchone()
