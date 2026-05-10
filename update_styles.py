import os

# 1. Update index.html
with open("public/index.html", "r") as f:
    content = f.read()

import re

# Replace style block
new_style = """<style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            color: #333;
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }

        h1 {
            font-size: 2.5rem;
            color: #e67e22;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            font-size: 1.2rem;
            color: #7f8c8d;
            margin-bottom: 1.5rem;
        }

        .nav-links {
            margin-bottom: 2rem;
        }

        .nav-links a {
            color: white;
            font-size: 1.1rem;
            text-decoration: none;
            background: #34495e;
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            margin: 0 10px;
            transition: background 0.2s;
        }

        .nav-links a:hover {
            background: #2c3e50;
        }

        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            max-width: 1000px;
            margin: 0 auto;
        }

        .card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 20px;
            width: 220px;
            color: #444;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #eaeaea;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }

        .emoji {
            font-size: 3.5rem;
            display: block;
            margin-bottom: 10px;
        }

        h2 { margin: 10px 0; font-size: 1.3rem; color: #2c3e50; }
        
        .desc { color: #7f8c8d; font-size: 0.95rem; min-height: 2.5em; }

        button {
            background-color: #e67e22;
            color: white;
            font-family: inherit;
            font-size: 1rem;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 8px;
            font-weight: 600;
            transition: background-color 0.2s;
            margin-top: 10px;
            width: 100%;
        }

        button:hover {
            background-color: #d35400;
        }

        .vote-count {
            font-size: 1.3rem;
            font-weight: bold;
            color: #e67e22;
            background: #fdf2e9;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            line-height: 45px;
            margin: 10px auto;
        }

        .add-section {
            background-color: #ffffff;
            padding: 20px;
            margin-top: 40px;
            border-radius: 16px;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            border: 1px solid #eaeaea;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .add-section h2 {
            color: #2c3e50;
            margin-top: 0;
            margin-bottom: 15px;
        }
        
        .input-group {
            display: flex;
            width: 100%;
            gap: 10px;
        }

        #new-option-input {
            font-family: inherit;
            font-size: 1rem;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #bdc3c7;
            flex: 1;
        }

        #new-option-input:focus {
            outline: none;
            border-color: #e67e22;
        }
        
        .add-btn {
            width: auto;
            margin-top: 0;
        }
    </style>"""
content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)

# Replace the HTML body header part
old_header = """    <h1>DESAYUNO DEL SEÑOR DE LOS JUGUITOS</h1>
    <p style="font-size: 1.5rem; color: #00ffcc; text-shadow: 2px 2px 0 #000;">
        Dice Kinder Gomita que vote
    </p>
    <p>
        <a href="/evaluation.html" style="color: white; font-size: 1.5rem; background: black; padding: 10px; border-radius: 10px;">👉 GO JUDGE FOOD HERE 👈</a>
        &nbsp;
        <a href="/history.html" style="color: white; font-size: 1.5rem; background: #330066; padding: 10px; border-radius: 10px;">📜 HISTORIAL 📜</a>
    </p>"""

new_header = """    <h1>Desayuno del Señor de los Juguitos</h1>
    <p class="subtitle">
        Elige tu desayuno favorito
    </p>
    <div class="nav-links">
        <a href="/evaluation.html">Calificar Platos</a>
        <a href="/history.html">Ver Historial</a>
    </div>"""

content = content.replace(old_header, new_header)

old_card_js = """<span class="emoji">${item.emoji}</span>
                    <h2>${item.name}</h2>
                    <p>${item.desc}</p>
                    <div class="vote-count">${item.votes}</div>
                    <button onclick="vote(${item.id})">GIMME! 👇</button>"""

new_card_js = """<span class="emoji">${item.emoji}</span>
                    <h2>${item.name}</h2>
                    <p class="desc">${item.desc}</p>
                    <div class="vote-count">${item.votes}</div>
                    <button onclick="vote(${item.id})">Votar</button>"""
content = content.replace(old_card_js, new_card_js)

old_add = """<div class="add-section">
        <h2>Seleccione otra opcion</h2>
        <input type="text" id="new-option-input" placeholder="Escribe tu desayuno...">
        <button onclick="addOption()">Añadir!</button>
    </div>"""

new_add = """<div class="add-section">
        <h2>¿Falta una opción?</h2>
        <div class="input-group">
            <input type="text" id="new-option-input" placeholder="Escribe tu desayuno...">
            <button class="add-btn" onclick="addOption()">Añadir</button>
        </div>
    </div>"""
content = content.replace(old_add, new_add)

with open("public/index.html", "w") as f:
    f.write(content)


# 2. Update evaluation.html
with open("public/evaluation.html", "r") as f:
    eval_content = f.read()

new_eval_style = """<style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            color: #333;
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        h1 {
            font-size: 2.5rem;
            color: #27ae60;
            margin-bottom: 1.5rem;
        }
        .nav-links {
            margin-bottom: 2rem;
        }
        .nav-links a {
            color: white;
            font-size: 1.1rem;
            text-decoration: none;
            background: #34495e;
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            margin: 0 10px;
            transition: background 0.2s;
        }
        .nav-links a:hover {
            background: #2c3e50;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            max-width: 1000px;
            margin: 0 auto;
        }
        .card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 20px;
            width: 300px;
            color: #444;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            border: 1px solid #eaeaea;
        }
        h2 { margin-top: 0; color: #2c3e50; }
        .score-display {
            font-size: 1.8rem;
            font-weight: bold;
            color: #27ae60;
            margin: 10px 0;
        }
        .buttons-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 5px;
            margin-bottom: 10px;
        }
        .rate-btn {
            width: 35px;
            height: 35px;
            border-radius: 50%;
            border: 1px solid #27ae60;
            background: #eafaf1;
            color: #27ae60;
            cursor: pointer;
            font-weight: bold;
            font-family: inherit;
            transition: all 0.2s;
        }
        .rate-btn:hover {
            background: #27ae60;
            color: white;
            transform: scale(1.1);
        }
    </style>"""

eval_content = re.sub(r'<style>.*?</style>', new_eval_style, eval_content, flags=re.DOTALL)

eval_old_header = """    <h1>⚖️ JUDGE THE FOOD ⚖️</h1>
    <a href="/">🔙 Back to Main Menu</a>
    <a href="/history.html" style="margin-left: 10px;">📜 Historial</a>"""

eval_new_header = """    <h1>Calificar Platos</h1>
    <div class="nav-links">
        <a href="/">Menú Principal</a>
        <a href="/history.html">Ver Historial</a>
    </div>"""
eval_content = eval_content.replace(eval_old_header, eval_new_header)

with open("public/evaluation.html", "w") as f:
    f.write(eval_content)


# 3. Update history.html
with open("public/history.html", "r") as f:
    hist_content = f.read()

new_hist_style = """<style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            color: #333;
            text-align: center;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }

        h1 {
            font-size: 2.5rem;
            color: #8e44ad;
            margin-bottom: 1.5rem;
        }

        .nav-links {
            margin-bottom: 2rem;
        }

        .nav-links a {
            color: white;
            font-size: 1.1rem;
            text-decoration: none;
            background: #34495e;
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            margin: 0 10px;
            transition: background 0.2s;
        }

        .nav-links a:hover {
            background: #2c3e50;
        }

        #app {
            max-width: 900px;
            margin: 0 auto;
        }

        .week-block {
            background: #ffffff;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 35px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            border: 1px solid #eaeaea;
        }

        .week-title {
            font-size: 1.4rem;
            color: #8e44ad;
            margin: 0 0 20px 0;
            border-bottom: 2px solid #f0f3f4;
            padding-bottom: 10px;
        }

        .meals-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }

        .meal-card {
            background: #fdfdfd;
            border: 1px solid #eaeaea;
            border-radius: 12px;
            padding: 20px;
            width: 200px;
            position: relative;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
            transition: transform 0.2s;
        }
        
        .meal-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.05);
        }

        .meal-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2c3e50;
            margin: 0 0 10px 0;
            min-height: 2.5rem;
        }

        .meal-score {
            font-size: 2.2rem;
            font-weight: bold;
            color: #8e44ad;
            line-height: 1;
            margin-bottom: 4px;
        }

        .meal-score-label {
            font-size: 0.85rem;
            color: #7f8c8d;
            margin-bottom: 12px;
        }

        .medal {
            font-size: 1.8rem;
            position: absolute;
            top: -12px;
            right: -10px;
            background: white;
            border-radius: 50%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .votes-badge {
            display: inline-block;
            background: #f4ecf7;
            color: #8e44ad;
            border-radius: 50px;
            padding: 4px 12px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .no-ratings {
            color: #bdc3c7;
            font-style: italic;
            font-size: 0.85rem;
        }

        #loading {
            font-size: 1.5rem;
            margin-top: 60px;
            color: #7f8c8d;
        }

        #error-msg {
            display: none;
            background: #e74c3c;
            color: white;
            padding: 20px;
            border-radius: 12px;
            font-size: 1.1rem;
            margin-top: 20px;
        }
    </style>"""

hist_content = re.sub(r'<style>.*?</style>', new_hist_style, hist_content, flags=re.DOTALL)

hist_old_header = """    <h1>📜 HISTORIAL DE DESAYUNOS 📜</h1>
    <a href="/" class="back-btn">🔙 Menu Principal</a>"""

hist_new_header = """    <h1>Historial de Desayunos</h1>
    <div class="nav-links">
        <a href="/">Menú Principal</a>
        <a href="/evaluation.html">Calificar Platos</a>
    </div>"""
hist_content = hist_content.replace(hist_old_header, hist_new_header)

with open("public/history.html", "w") as f:
    f.write(hist_content)

print("Styles updated successfully.")
