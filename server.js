require('dotenv').config();
const express = require('express');
const http    = require('http');

const app  = express();
const port = 3000;
const PYTHON_PORT = 5001;

app.use(express.json());
app.use(express.static('public'));

// ---------------------------------------------------------------------------
// Helper: call Python Oracle API
// ---------------------------------------------------------------------------
function pythonRequest(method, path, body = null) {
    return new Promise((resolve, reject) => {
        const bodyStr = body ? JSON.stringify(body) : null;
        const options = {
            hostname: 'localhost',
            port: PYTHON_PORT,
            path,
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (bodyStr) options.headers['Content-Length'] = Buffer.byteLength(bodyStr);

        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve({ status: res.statusCode, body: JSON.parse(data) }));
        });
        req.on('error', reject);
        if (bodyStr) req.write(bodyStr);
        req.end();
    });
}

// ---------------------------------------------------------------------------
// VOTING (in-memory)
// ---------------------------------------------------------------------------
let breakfastOptions = [
    { id: 1, name: 'Tacos de Barbacoa junto al Oxxo', emoji: '🌮', votes: 0, desc: 'Super spicy & yummy!' },
    { id: 2, name: 'Tacos del Chino', emoji: '🥡', votes: 0, desc: 'Mystery meat goodness!' },
    { id: 3, name: 'Chilaquiles', emoji: '🍳', votes: 0, desc: 'Greasy hashbrowns!' },
    { id: 4, name: 'Burrito de Machacado', emoji: '🌯', votes: 0, desc: 'A new challenger!' }
];

app.get('/api/breakfasts', (req, res) => {
    res.json(breakfastOptions);
});

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

app.post('/api/add-option', (req, res) => {
    const { name } = req.body;
    if (!name || name.trim() === '') {
        return res.status(400).json({ success: false, message: 'Option name cannot be empty!' });
    }
    const newId = breakfastOptions.length > 0 ? Math.max(...breakfastOptions.map(o => o.id)) + 1 : 1;
    const newOption = { id: newId, name: name.trim(), emoji: '😋', votes: 0, desc: 'A new challenger!' };
    breakfastOptions.push(newOption);
    res.status(201).json({ success: true, item: newOption });
});

// ---------------------------------------------------------------------------
// EVALUATIONS — proxied to Python Oracle API
// ---------------------------------------------------------------------------
app.get('/api/evaluations', async (req, res) => {
    try {
        const r = await pythonRequest('GET', '/evaluations');
        res.status(r.status).json(r.body);
    } catch (err) {
        console.error('GET /api/evaluations error:', err.message);
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/rate', async (req, res) => {
    try {
        const r = await pythonRequest('POST', '/rate', req.body);
        res.status(r.status).json(r.body);
    } catch (err) {
        console.error('POST /api/rate error:', err.message);
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/options', async (req, res) => {
    try {
        const r = await pythonRequest('POST', '/options', req.body);
        res.status(r.status).json(r.body);
    } catch (err) {
        console.error('POST /api/options error:', err.message);
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/history', async (req, res) => {
    try {
        const r = await pythonRequest('GET', '/history');
        res.status(r.status).json(r.body);
    } catch (err) {
        console.error('GET /api/history error:', err.message);
        res.status(500).json({ error: err.message });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
