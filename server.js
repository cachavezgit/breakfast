require('dotenv').config();
const express = require('express');
const oracledb = require('oracledb');
const { getConnection } = require('./db');

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

// In-memory database (resets when server restarts)
let breakfastOptions = [
    { id: 1, name: 'Tacos de Barbacoa junto al Oxxo', emoji: '🌮', votes: 0, desc: 'Super spicy & yummy!' },
    { id: 2, name: 'Tacos del Chino', emoji: '🥡', votes: 0, desc: 'Mystery meat goodness!' },
    { id: 3, name: 'Desayuno McDonalds', emoji: '🍟', votes: 0, desc: 'Greasy hashbrowns!' }
];

// API: Get current votes
app.get('/api/breakfasts', (req, res) => {
    res.json(breakfastOptions);
});

// API: Cast a vote
app.post('/api/vote', (req, res) => {
    const { id } = req.body;
    const item = breakfastOptions.find(b => b.id === id);

    if (item) {
        item.votes += 1;
        res.json({ success: true, item });
    } else {
        res.status(404).json({ success: false, message: 'Not found!' });
    }
});

// API: Add a new option
app.post('/api/add-option', (req, res) => {
    const { name } = req.body;

    if (!name || name.trim() === '') {
        return res.status(400).json({ success: false, message: 'Option name cannot be empty!' });
    }

    const newId = breakfastOptions.length > 0 ? Math.max(...breakfastOptions.map(o => o.id)) + 1 : 1;

    const newOption = {
        id: newId,
        name: name.trim(),
        emoji: '😋',
        votes: 0,
        desc: 'A new challenger!'
    };
    breakfastOptions.push(newOption);
    res.status(201).json({ success: true, item: newOption });
});

// ---------------------------------------------------------------------------
// EVALUATIONS — Oracle DB
// ---------------------------------------------------------------------------

// GET /api/evaluations — opciones de la semana activa con promedio y conteo
app.get('/api/evaluations', async (req, res) => {
    let conn;
    try {
        conn = await getConnection();
        const result = await conn.execute(
            `SELECT o.id, o.name,
                    COUNT(r.id)          AS "count",
                    ROUND(AVG(r.score), 1) AS "average"
             FROM meal_options o
             LEFT JOIN meal_ratings r ON r.option_id = o.id
             WHERE SYSDATE BETWEEN o.week_start AND o.week_end
             GROUP BY o.id, o.name
             ORDER BY o.id`,
            [],
            { outFormat: oracledb.OUT_FORMAT_OBJECT }
        );
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    } finally {
        if (conn) await conn.close();
    }
});

// POST /api/rate — guardar calificación
app.post('/api/rate', async (req, res) => {
    const { id, score } = req.body;
    if (!id || score < 0 || score > 10) {
        return res.status(400).json({ error: 'Invalid rating' });
    }
    let conn;
    try {
        conn = await getConnection();
        await conn.execute(
            `INSERT INTO meal_ratings (option_id, score) VALUES (:id, :score)`,
            { id, score },
            { autoCommit: true }
        );
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: err.message });
    } finally {
        if (conn) await conn.close();
    }
});

// POST /api/options — cargar opciones de una nueva semana
// Body: { week_start: 'YYYY-MM-DD', week_end: 'YYYY-MM-DD', options: [{ name }] }
app.post('/api/options', async (req, res) => {
    const { options, week_start, week_end } = req.body;
    if (!options || !week_start || !week_end) {
        return res.status(400).json({ error: 'options, week_start y week_end son requeridos' });
    }
    let conn;
    try {
        conn = await getConnection();
        for (const opt of options) {
            await conn.execute(
                `INSERT INTO meal_options (name, week_start, week_end)
                 VALUES (:name, TO_DATE(:week_start, 'YYYY-MM-DD'), TO_DATE(:week_end, 'YYYY-MM-DD'))`,
                { name: opt.name, week_start, week_end },
                { autoCommit: true }
            );
        }
        res.json({ success: true, inserted: options.length });
    } catch (err) {
        res.status(500).json({ error: err.message });
    } finally {
        if (conn) await conn.close();
    }
});

// GET /api/history — historial de calificaciones agrupado por semana y opción
app.get('/api/history', async (req, res) => {
    let conn;
    try {
        conn = await getConnection();
        const result = await conn.execute(
            `SELECT o.name,
                    TO_CHAR(o.week_start, 'YYYY-MM-DD') AS "week_start",
                    TO_CHAR(o.week_end,   'YYYY-MM-DD') AS "week_end",
                    COUNT(r.id)                          AS "count",
                    ROUND(AVG(r.score), 1)               AS "average"
             FROM meal_options o
             LEFT JOIN meal_ratings r ON r.option_id = o.id
             GROUP BY o.name, o.week_start, o.week_end
             ORDER BY o.week_start DESC, o.name`,
            [],
            { outFormat: oracledb.OUT_FORMAT_OBJECT }
        );
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    } finally {
        if (conn) await conn.close();
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
