import sqlite3
from pathlib import Path

CURRENT_FOLDER = Path(__file__).resolve().parent 
PROJECT_ROOT = CURRENT_FOLDER.parent
DATABASE_FOLDER = PROJECT_ROOT / "database"




con = sqlite3.connect(DATABASE_FOLDER/"database.db")

cur = con.cursor()

cur.execute(" CREATE TABLE IF NOT EXISTS " 
            "Poll "
"( poll_id TEXT PRIMARY KEY, " 
"poll_name VARCHAR(255) NOT NULL, " 
"participant_limit INTEGER NOT NULL, " 
"start_date DATE NOT NULL," 
" start_time TIME NOT NULL, " 
"deadline TIME NOT NULL," 
" password_hash VARCHAR(255) NOT NULL)" 
"")



cur.execute(" CREATE TABLE IF NOT EXISTS " 
            "PollDate " 
            "( poll_id TEXT NOT NULL, " 
            "date DATE NOT NULL, " 
            "PRIMARY KEY (poll_id, date), " 
            "FOREIGN KEY (poll_id) REFERENCES Poll(poll_id) )" 
            "")


cur.execute(" CREATE TABLE IF NOT EXISTS " 
            "Participant " 
                "( participant_id TEXT PRIMARY KEY, " 
                "poll_id TEXT NOT NULL, " 
                "participant_name VARCHAR(255) NOT NULL COLLATE NOCASE, " 
                "is_creator BOOLEAN NOT NULL, " 
                "FOREIGN KEY (poll_id) REFERENCES Poll(poll_id)," 
                "UNIQUE (poll_id, participant_name) )" )


cur.execute(" CREATE TABLE IF NOT EXISTS " 
            "Selection " 
                "( poll_id TEXT NOT NULL, " 
                "participant_id TEXT NOT NULL, "
                "date DATE NOT NULL, " 
                "slot_start_time TIME NOT NULL, " 
                "FOREIGN KEY (poll_id) REFERENCES Poll(poll_id), " 
                "FOREIGN KEY (participant_id) REFERENCES Participant(participant_id), " 
                "PRIMARY KEY (poll_id, participant_id, date, slot_start_time))")




