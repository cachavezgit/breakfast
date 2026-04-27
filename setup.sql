-- Run this once in Oracle to create the tables and load the current week's options

CREATE TABLE meal_options (
    id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR2(200) NOT NULL,
    week_start  DATE NOT NULL,
    week_end    DATE NOT NULL
);

CREATE TABLE meal_ratings (
    id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    option_id   NUMBER NOT NULL REFERENCES meal_options(id),
    score       NUMBER(4,1) NOT NULL,
    rated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Semana actual: 27 Abril - 3 Mayo 2026
INSERT INTO meal_options (name, week_start, week_end) VALUES ('Hamburguesa, papas caseras y sopa de codito', TO_DATE('2026-04-27', 'YYYY-MM-DD'), TO_DATE('2026-05-03', 'YYYY-MM-DD'));
INSERT INTO meal_options (name, week_start, week_end) VALUES ('Tacos del Chava',                            TO_DATE('2026-04-27', 'YYYY-MM-DD'), TO_DATE('2026-05-03', 'YYYY-MM-DD'));
INSERT INTO meal_options (name, week_start, week_end) VALUES ('Desayuno McDonald''s',                       TO_DATE('2026-04-27', 'YYYY-MM-DD'), TO_DATE('2026-05-03', 'YYYY-MM-DD'));
INSERT INTO meal_options (name, week_start, week_end) VALUES ('Pizzita de la Sierra',                       TO_DATE('2026-04-27', 'YYYY-MM-DD'), TO_DATE('2026-05-03', 'YYYY-MM-DD'));
INSERT INTO meal_options (name, week_start, week_end) VALUES ('Botanita',                                   TO_DATE('2026-04-27', 'YYYY-MM-DD'), TO_DATE('2026-05-03', 'YYYY-MM-DD'));
INSERT INTO meal_options (name, week_start, week_end) VALUES ('Fruta',                                      TO_DATE('2026-04-27', 'YYYY-MM-DD'), TO_DATE('2026-05-03', 'YYYY-MM-DD'));
COMMIT;
