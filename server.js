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

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    console.log('Go vote for brekkie!');
});
