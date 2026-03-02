from database import init_db, add_record, get_all_records

init_db()

add_record("2026-03-02", "AI", 3, 8, 5, 9.0)

print(get_all_records())