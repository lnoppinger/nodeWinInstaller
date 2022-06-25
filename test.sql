CREATE TABLE einheit (
    id SERIAL PRIMARY KEY,
    name varchar(5)
);
INSERT INTO einheit (
    name
) VALUES
(
    'kg'
),
(
    'g'
),
(
    'l'
),
(
    'ml'
),
(
    'St.'
),
(
    '%'
);

CREATE TABLE rezept_art (
    id SERIAL PRIMARY KEY,
    name varchar(30)
);
INSERT INTO rezept_art (
    name
) VALUES
(
    'Zutat'
),
(
    'Zwischenrezept'
),
(
    'Rezept'
);

CREATE TABLE rezept (
    id serial PRIMARY KEY,
    name varchar(30),
    einheit_id int REFERENCES einheit(id) ON DELETE CASCADE,
    rezept_art_id int REFERENCES rezept_art(id) ON DELETE CASCADE,
    menge int
);

CREATE TABLE zutat (
    id SERIAL PRIMARY KEY,
    name varchar(30),
    rezept_id int REFERENCES rezept(id) ON DELETE CASCADE,
    anteil int,
    preis int,
    datum char(10)
);

CREATE TABLE rezept_map (
    id SERIAL PRIMARY KEY,
    zutat_id int REFERENCES rezept(id) ON DELETE CASCADE,
    rezept_id int REFERENCES rezept(id) ON DELETE CASCADE,
    menge int
)