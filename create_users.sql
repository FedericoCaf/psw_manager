-- DROP TABLE IF EXISTS passwords;

-- CREATE TABLE passwords (
--     id INTEGER PRIMARY KEY,
--     user_id INTEGER,
--     context VARCHAR(255),
--     username VARCHAR(100),
--     password VARCHAR(100),
--     FOREIGN KEY (user_id) REFERENCES users(id)
-- );


DELETE FROM passwords WHERE id > 2;

-- INSERT INTO users (nome, cognome, email, username, password, data_iscrizione) VALUES (
--    'marcorossi@gmail.com','marco92', 'marco92', '2023-01-01'
-- );
-- INSERT INTO users (nome, cognome, email, username, password, data_iscrizione) VALUES (
--    'lindabianchi@gmail.com','linda87', 'linda87', '2023-02-01'
-- );
-- INSERT INTO users (nome, cognome, email, username, password, data_iscrizione) VALUES (
--    'giannibardi@gmail.com','gianni77', 'gianni77', '2023-03-01'
-- );