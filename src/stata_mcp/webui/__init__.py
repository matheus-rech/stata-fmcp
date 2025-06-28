from flask import Flask, redirect, render_template, request, url_for

from ..config import Config

app = Flask(__name__, static_folder="templates")
config_mgr = Config()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    saved = request.args.get('saved') == '1'
    if request.method == 'POST':
        stata_cli = request.form['stata_cli']
        output_base_path = request.form['output_base_path']
        config_mgr.set('stata.stata_cli', stata_cli)
        config_mgr.set('stata-mcp.output_base_path', output_base_path)
        return redirect(url_for('config', saved='1'))

    return render_template(
        'config.html',
        stata_cli=config_mgr.get('stata.stata_cli', ''),
        output_base_path=config_mgr.get('stata-mcp.output_base_path', ''),
        saved=saved
    )


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
