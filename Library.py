from Database import Database
import datetime

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
    
    def create_new_user(self, google_id: str):
        account_metadata = {
            "date_registered": datetime.datetime.now().timestamp()
        }
        
        sql_query = f"""
        INSERT INTO public."Users" (google_id, account_metadata)
        VALUES (%s, %s);
        """
        self.database.execute_sql_query(sql_query, args=(google_id, account_metadata))

    def retrieve_user_by_google_id(self, google_id: str):
        sql_query = f"""
        SELECT google_id, account_metadata, date_created FROM public."Users" WHERE google_id = %s
        """
        cursor = self.database.execute_sql_query(sql_query, args=(google_id,))
        return cursor.fetchone()
