from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/save_config', methods=['POST'])
def save_config():
    stata_path = request.form['stata_path']
    model_category = request.form['model_category']

    # 处理模型类别
    if model_category == 'ollama':
        result = "A"
    elif model_category == 'OpenAI':
        result = "B"

    return redirect(url_for('config', stata_path=stata_path, model_category=model_category))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
