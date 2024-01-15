from flask import Flask, request, jsonify

app = Flask(__name__)
proxy_list = []


@app.route('/', methods=['GET'])
def index():
    return 'Welcome to Proxy Server!'


@app.route('/proxy', methods=['GET'])
def get_proxy():
    def get_proxy():
        global current_index
        proxy = proxy_list[current_index]
        current_index = (current_index + 1) % len(proxy_list)
        return proxy


    proxy = proxy_list.pop(0)
    return proxy


def start_proxy_server(proxies):
    global proxy_list
    proxy_list = proxies
    app.run(host='127.0.0.1', port=5552)


if __name__ == '__main__':
    start_proxy_server([])
