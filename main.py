import random
import string
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
# To store the urls
shortend_urls: dict = {}


def generate_short_url(length: int = 6) -> str:
    chars = string.ascii_letters+string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_url = generate_short_url()
        while short_url in shortend_urls:
            short_url = generate_short_url()

        shortend_urls[short_url] = original_url
        return f' Short URL: <a href="{request.url_root}{short_url}" target="_blank">{request.url_root}{short_url}</a>'
    return render_template('index.html')


@app.route('/<short_url>')
def redirect_to_url(short_url: str):
    original_url = shortend_urls.get(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return f"URL for {short_url} not found", 404


if __name__ == '__main__':
    app.run()
