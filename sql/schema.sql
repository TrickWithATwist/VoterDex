PRAGMA foreign_keys = ON;

CREATE TABLE candidate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    affiliation TEXT NOT NULL
);