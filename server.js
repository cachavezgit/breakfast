const express = require('express');
const app = express();
const port = 3000;

// Middleware to parse JSON bodies and serve static files
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

// In-memory database for evaluations
let evaluationOptions = [
    { id: 1, name: 'Tostadas de Tinga de Pollo', ratings: [] },
    { id: 2, name: 'La Papada del Mike', ratings: [] },
    { id: 3, name: 'Tacos de Barbacoa JC', ratings: [] },
    { id: 4, name: 'Country Taco', ratings: [] },
    { id: 5, name: 'Fruta', ratings: [] },
    { id: 6, name: 'Botanita', ratings: [] }
];

// API: Get evaluations
app.get('/api/evaluations', (req, res) => {
    const results = evaluationOptions.map(item => {
        const sum = item.ratings.reduce((a, b) => a + b, 0);
        const avg = item.ratings.length > 0 ? (sum / item.ratings.length).toFixed(1) : 0;
        return { ...item, average: avg, count: item.ratings.length };
    });
    res.json(results);
});

// API: Submit rating
app.post('/api/rate', (req, res) => {
    const { id, score } = req.body;
    const item = evaluationOptions.find(i => i.id === id);
    if (item && score >= 0 && score <= 10) {
        item.ratings.push(score);
        res.json({ success: true });
    } else {
        res.status(400).json({ error: 'Invalid rating' });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    console.log('Go vote for brekkie!');
});
