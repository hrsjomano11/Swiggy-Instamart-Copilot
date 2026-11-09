"""Validate Part A against the brief's reference checkpoints.
Run after part_a_clean.py:  python src/part_a_validate.py"""

import sqlite3
import pandas as pd

o = pd.read_csv("data/clean/orders.csv")
c = pd.read_csv("data/clean/customers.csv")
with sqlite3.connect("data/instamart.db") as con:
    tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    db_rows = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

done = o[o["status"] == "completed"]
canc = o[o["status"] == "cancelled"]

assert {"customers", "products", "orders"} <= tables, "missing DB tables"
assert db_rows == 12309, "DB orders row count"
assert len(o) == 12309 and o["order_id"].is_unique, "orders: one row per order_id"
assert len(done) == 11110 and len(canc) == 1199, "completed/cancelled split"
assert not (o["status"] == "pending").any(), "pending rows remain"
assert o["order_amount"].isna().sum() == 0, "missing order_amount"
assert done["delivery_minutes"].isna().sum() == 0, "missing delivery (completed)"
assert canc["delivery_minutes"].isna().sum() == 1199, "cancelled delivery should stay missing"
assert round(done["order_amount"].sum(), 2) == 2998668.80, "completed revenue"
assert c["city"].nunique() == 6, "six cities"
assert c["city"].value_counts().to_dict() == {"Pune": 227, "Delhi": 210, "Bengaluru": 197,
                                              "Chennai": 191, "Hyderabad": 191, "Mumbai": 184}, "city counts"
assert c["gender"].value_counts().to_dict() == {"female": 610, "male": 560, "unknown": 30}, "gender counts"
assert c["age"].isna().sum() == 0 and c["age"].between(18, 60).all(), "ages"
part_a_validate.py     # should print: ALL CHECKPOINTS PASSED
print("ALL CHECKPOINTS PASSED")