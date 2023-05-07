CREATE TABLE "Minimax_Cache" (
        primary_key INTEGER NOT NULL, 
        board_state_hash VARCHAR, 
        depth INTEGER, 
        score INTEGER, 
        move VARCHAR, 
        PRIMARY KEY (primary_key)
);
CREATE TABLE "Saved_Games" (
        primary_key INTEGER NOT NULL, 
        cookie_key VARCHAR, 
        raw_game_data BINARY, 
        PRIMARY KEY (primary_key)
);
CREATE INDEX board_state_hash ON "Minimax_Cache" (board_state_hash);
CREATE INDEX cookie_key ON "Saved_Games" (cookie_key);