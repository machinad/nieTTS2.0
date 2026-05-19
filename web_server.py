from quart import Quart,render_template,request,jsonify,send_file,send_from_directory
import os
class WebServer:
    def __init__(self,):
        self.app = Quart(__name__)
        self.app.route('/')(self.index)
        self.app.route('/tts', methods=['POST'])(self.tts_endpoint)
        self.app.route('/save_provider')(self.save_provider)
        self.app.route('/save_edgetts_voices')(self.save_edgetts_voices)
        self.app.route('/templates/<path:filename>')(self.serve_static)
    async def index(self):
        pass
    async def tts_endpoint(self):
        pass
    async def save_provider(self):
        pass
    async def save_edgetts_voices(self):
        pass
    async def serve_static(self):
        pass
    def run(self,host='127.0.0.1',port=11451):
        self.app.run(host=host,port=port)

        