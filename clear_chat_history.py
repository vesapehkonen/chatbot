from tinydb import TinyDB, Query
import argparse

def clear_history(db_path, user=None):
    db = TinyDB(db_path)
    messages_table = db.table('messages')

    if user:
        Message = Query()
        deleted = messages_table.remove(Message.user == user)
        print(f"Deleted {len(deleted)} messages for user '{user}'.")
    else:
        count = len(messages_table)
        messages_table.truncate()
        print(f"Deleted all ({count}) messages.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clear chat history from TinyDB.")
    parser.add_argument("--user", help="Username to delete messages for (optional)")
    parser.add_argument("--db", default="chat_memory.json", help="Path to TinyDB file")

    args = parser.parse_args()
    clear_history(args.db, args.user)
