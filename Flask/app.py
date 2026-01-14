from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Name Transformer</title>
    <style>
        body {
            background: linear-gradient(120deg, #4facfe, #00f2fe);
            font-family: Arial;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            width: 350px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        input {
            width: 80%;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #aaa;
            margin-bottom: 10px;
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            background: #4facfe;
            color: white;
            cursor: pointer;
        }

        .result {
            margin-top: 20px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔥 Name Transformer 🔥</h2>

        <form action="/" method="get">
            <input type="text" name="name" placeholder="Enter your name" required>
            <br>
            <button>Transform</button>
        </form>

        {% if name %}
        <div class="result">
            <p><b>Original:</b> {{ name }}</p>
            <p><b>UPPERCASE:</b> {{ name.upper() }}</p>
            <p><b>Length:</b> {{ name|length }}</p>
            <p><b>Reversed:</b> {{ name[::-1] }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    name = request.args.get('name')
    return render_template_string(TEMPLATE, name=name)

if __name__ == '__main__':
    app.run(debug=True)
