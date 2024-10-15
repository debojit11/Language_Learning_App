# main.py
from gui import main  # Import the main function from gui
from database import setup_database, connect_db  # Import connect_db function
import sys
import traceback  # Import traceback for detailed error messages

def main_app():
    db_connection = None  # Initialize db_connection to ensure it's defined in finally block

    try:
        setup_database()  # Initialize the database
        db_connection = connect_db()  # Connect to the database
        if db_connection is None:
            raise Exception("Failed to connect to the database.")
    except Exception as e:
        print(f"Error setting up the database: {e}")
        traceback.print_exc()  # Print the traceback for the database setup error
        sys.exit(1)  # Exit if the database setup fails
    
    try:
        main()  # Launch the GUI main function with the connection
    except Exception as e:
        print(f"Error launching the GUI: {e}")
        traceback.print_exc()  # Print the traceback for the GUI error
        sys.exit(1)  # Exit if GUI fails to start
    finally:
        if db_connection:
            db_connection.close()  # Close the connection when done

if __name__ == "__main__":
    main_app()
