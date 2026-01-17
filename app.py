
from quart import Quart,render_template,request,jsonify,send_file
import os
import win32com.client
import edge_tts
import uuid
import pygame
import json
import queue
import threading
import io
import sys
import httpx
import subprocess
import socket
import atexit
import asyncio
import torch
from pythonosc import udp_client
from pathlib import Path
import dashscope 
import gc
import sounddevice as sd
from dashscope.audio.tts_v2 import SpeechSynthesizer as SpeechSynthesizerV2
from dashscope.audio.tts import SpeechSynthesizer as SpeechSynthesizerV1
import time
from multiprocessing import freeze_support
from indextts.infer import IndexTTS  # noqa: E402
class TTSWebApp:
    def __init__(self):
        self.text_split_method = {
            "不切":"cut0",
            "凑四句一切":"cut1",
            "凑50字一切":"cut2",
            "按中文句号。切":"cut3",
            "按英文句号.切":"cut4",
            "按标点符号切":"cut5"
        }
        self.Edge_TTS_voices = [
            # 女声
            "zh-CN-XiaoxiaoNeural",  # Female, News/Novel, Warm
            "zh-CN-XiaoyiNeural",    # Female, Cartoon/Novel, Lively
            "zh-CN-liaoning-XiaobeiNeural",  # Female, Dialect, Humorous
            "zh-CN-shaanxi-XiaoniNeural",   # Female, Dialect, Bright
            
            # 男声
            "zh-CN-YunjianNeural",   # Male, Sports/Novel, Passion
            "zh-CN-YunxiNeural",     # Male, Novel, Lively/Sunshine
            "zh-CN-YunxiaNeural",    # Male, Cartoon/Novel, Cute
            "zh-CN-YunyangNeural"    # Male, News, Professional/Reliable
        ]
        self.ali_tts_voices = {
            "龙婉-普通话-语音助手、导航播报、聊天数字人":"longwan",
            "龙橙-普通话-语音助手、导航播报、聊天数字人":"longcheng",
            "龙华-普通话-语音助手、导航播报、聊天数字人":"longhua",
            "龙小淳-普通话+英文-语音助手、导航播报、聊天数字人":"longxiaochun",
            "龙小夏-普通话-语音助手、聊天数字人":"longxiaoxia",
            "龙小诚-普通话+英文-语音助手、导航播报、聊天数字人":"longxiaocheng",
            "龙小白-普通话-聊天数字人、有声书、语音助手":"longxiaobai",
            "龙老铁-东北口音-新闻播报、有声书、语音助手、直播带货、导航播报":"longlaotie",
            "龙书-普通话-有声书、语音助手、导航播报、新闻播报、智能客服":"longshu",
            "龙硕-普通话-语音助手、导航播报、新闻播报、客服催收":"longshuo",
            "龙婧-普通话-语音助手、导航播报、新闻播报、客服催收":"longjing",
            "龙妙-普通话-客服催收、导航播报、有声书、语音助手":"longmiao",
            "龙悦-普通话-语音助手、诗词朗诵、有声书朗读、导航播报、新闻播报、客服催收":"longyue",
            "龙媛-普通话-有声书、语音助手、聊天数字人":"longyuan",
            "龙飞-普通话-会议播报、新闻播报、有声书":"longfei",
            "龙杰力豆-普通话+英文-新闻播报、有声书、聊天助手":"longjielidou",
            "龙彤-普通话-有声书、导航播报、聊天数字人":"longtong",
            "龙祥-普通话-新闻播报、有声书、导航播报":"longxiang",
            "Stella-普通话+英文-语音助手、直播带货、导航播报、客服催收、有声书":"loongstella",
            "Bella-普通话-语音助手、客服催收、新闻播报、导航播报":"loongbella"
        }
        self.sambert_tts_voices = {
            "知琪-温柔女声-通用场景":"sambert-zhiqi-v1",
            "知佳-标准女声-新闻播报":"sambert-zhijia-v1",
            "知茹-新闻女声-新闻播报":"sambert-zhiru-v1",
            "知倩-资讯女声-配音解说、新闻播报":"sambert-zhiqian-v1",
            "知薇-萝莉女声-阅读产品简介":"sambert-zhiwei-v1",
            "知婧-严厉女声-通用场景":"sambert-zhijing-v1",
            "知娜-浙普女声-通用场景":"sambert-zhina-v1",
            "知莎-知性女声-通用场景":"sambert-zhistella-v1",
            "知婷-电台女声-通用场景":"sambert-zhiting-v1",
            "知笑-资讯女声-通用场景":"sambert-zhixiao-v1",
            "知雅-严厉女声-通用场景":"sambert-zhiya-v1",
            "知媛-知心姐姐-通用场景":"sambert-zhiyuan-v1",
            "知颖-软萌童声-通用场景":"sambert-zhiying-v1",
            "知悦-温柔女声-客服":"sambert-zhiyue-v1",
            "知柜-直播女声-阅读产品简介":"sambert-zhigui-v1",
            "知妙（多情感）-多种情感女声-阅读产品简介、数字人、直播":"sambert-zhimiao-emo-v1",
            "知猫-直播女声-阅读产品简介、配音解说、数字人、直播":"sambert-zhimao-v1",
            "知楠-广告男声-通用场景":"sambert-zhinan-v1",
            "知厨-舌尖男声-新闻播报":"sambert-zhichu-v1",
            "知德-新闻男声-新闻播报":"sambert-zhide-v1",
            "知祥-磁性男声-配音解说":"sambert-zhixiang-v1",
            "知浩-咨询男声-通用场景":"sambert-zhihao-v1",
            "知茗-诙谐男声-通用场景":"sambert-zhiming-v1",
            "知墨-情感男声-通用场景":"sambert-zhimo-v1",
            "知树-资讯男声-通用场景":"sambert-zhishu-v1", 
            "知晔-青年男声-通用场景":"sambert-zhiye-v1",
            "知硕-自然男声-数字人":"sambert-zhishuo-v1",
            "知伦-悬疑解说-配音解说":"sambert-zhilun-v1",
            "知飞-激昂解说-配音解说":"sambert-zhifei-v1",
            "知达-标准男声-新闻播报":"sambert-zhida-v1",
            "Camila-西班牙语女声-通用场景":"sambert-camila-v1",
            "Perla-意大利语女声-通用场景":"sambert-perla-v1",
            "Indah-印尼语女声-通用场景":"sambert-indah-v1",
            "Clara-法语女声-通用场景":"sambert-clara-v1",
            "Hanna-德语女声-通用场景":"sambert-hanna-v1",
            "Beth-咨询女声-通用场景":"sambert-beth-v1",
            "Betty-客服女声-通用场景":"sambert-betty-v1",
            "Cally-自然女声-通用场景":"sambert-cally-v1",
            "Cindy-对话女声-通用场景":"sambert-cindy-v1",
            "Eva-陪伴女声-通用场景":"sambert-eva-v1",
            "Donna-教育女声-通用场景":"sambert-donna-v1",
            "Brian-客服男声-通用场景":"sambert-brian-v1",
            "Waan-泰语女声-通用场景":"sambert-waan-v1"
        }
        self.config_file = Path("./config.json")
        self.rvc_config_file = Path("./configs/config.json")
        self.rvc_weights_path = Path("./assets/weights").resolve()
        self.rvc_index_path = Path("./logs").resolve()
        self.index_path = Path("./checkpoints").resolve()
        self.local_tts_process = None
        self.GPTvts_voices_path = Path("./GPTvts_voices").resolve()
        self.GPTvts_path = Path("./GPTvts").resolve()
        self.rvcIndex_path = Path("./logs").resolve()
        self.savePath = Path("./save").resolve()
        self.GPTvts_name = "GPT-SoVITS-v4-20250422fix"
        self.GPTvts_modelPath = Path("./GPTvts/GPT-SoVITS-v4-20250422fix/GPT_SoVITS/pretrained_models").resolve()
        self.local_interpreter_path = os.path.join(self.GPTvts_path, "GPT-SoVITS-v4-20250422fix",'runtime', 'python.exe')
        self.local_script_path = os.path.join(self.GPTvts_path,"GPT-SoVITS-v4-20250422fix",'api_v2.py')
        self.local_script_cwd = os.path.join(self.GPTvts_path,"GPT-SoVITS-v4-20250422fix")
        try:
            self.rvcIndex_path.mkdir(parents=True, exist_ok=True)
            self.GPTvts_path.mkdir(parents=True, exist_ok=True)
            print(f"创建目录{self.GPTvts_modelPath}成功")
        except Exception as e:
            print(f"创建目录{self.GPTvts_path}失败: {e}")
        try:
            self.GPTvts_voices_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"创建目录{self.GPTvts_voices_path}失败: {e}")
        try:
            self.savePath.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"创建目录{self.savePath}失败: {e}")
        self.user_config = self.load_config()
        self.user_rvc_config = self.load_rvc_config()
        self.app = Quart(__name__)
        self.current_device = "default"
        self.tts_providers = [
            "Edge TTS",
            "阿里百炼cosyvice",
            "阿里百炼sambert",
            "GPTvts本地推理",
            "Index TTS",
            "RVC变声器"
        ]
        
        self.setup_routes()
        self.index_tts = None
        self.rvc_server = None
        self.osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
        atexit.register(self.cleanup)
    os.makedirs('templates', exist_ok=True) 
    def load_config(self):
        """
        加载配置
        """
        default_config = {
            "provider":"Edge TTS",
            "edge_tts_voice":"zh-CN-XiaoxiaoNeural",
            "device":"默认设备",
            "ali_tts_voice":"龙婉-普通话-语音助手、导航播报、聊天数字人",
            "sambert_tts_voice":"知婧-严厉女声-通用场景",
            "ali_api_key":"",
            "GPTvts_character": "",
            "GPTvts_emotion": "",
            "GPTvts_sample": "",
            "GPTvts_speed_factor":1,
            "GPTvts_temperature_factor":1,
            "GPTvts_text_split_method":"按中文句号。切",
            "GPTmodelName":"",
            "SovitsModelName":"",
            "parallel_infer":True,
            "split_bucket":True,
            "batch_size_slider":5,
            "batch_threshold_slider":0.75,
            "isdownload":False,
            "isplayaudio":True,
            "isIndex_tts_flash":False
        }
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                print(f"tts加载配置文件失败: {e}")
                return default_config
        return default_config
    def load_rvc_config(self):
        """
        加载RVC配置
        """
        default_config = {
            "pth_path": "assets/weights/kikiV1.pth",
            "index_path": "logs/kikiV1.index", 
            "sg_hostapi": "MME", 
            "sg_wasapi_exclusive": False, 
            "sg_input_device": "VoiceMeeter Output (VB-Audio Vo", 
            "sg_output_device": "VoiceMeeter Input (VB-Audio Voi", 
            "sr_type": "sr_device", 
            "threhold": -60.0, 
            "pitch": 12.0, 
            "formant": 0.0, 
            "rms_mix_rate": 0.5, 
            "index_rate": 0.0, 
            "block_time": 0.15, 
            "crossfade_length": 0.08, 
            "extra_time": 2.0, 
            "n_cpu": 4.0, 
            "use_jit": False, 
            "use_pv": False, 
            "f0method": "fcpe"
            }
        if self.rvc_config_file.exists():
            try:
                with open(self.rvc_config_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return default_config
        return default_config
    def save_config(self,config):
        """
        保存配置
        """
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as file:
                json.dump(config, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    def setup_routes(self):
        """
        返回html前端模板，渲染前端页面
        """
        self.app.route('/')(self.index)
        """
        /tts,POST请求，处理tts请求,
        """
        self.app.route('/tts', methods=['POST'])(self.tts_endpoint)
        self.app.route("/get_voice_list")(self.get_voice_list)
        self.app.route("/GPTvts_tts_start")(self.GPTvts_tts_start)
        self.app.route("/check_GPTvts_is_open")(self.check_GPTvts_is_open)
        self.app.route("/selectModel",methods=["POST"])(self.selectModel)
        self.app.route("/index_tts_start")(self.index_tts_start)
        self.app.route("/check_index_tts")(self.check_index_tts)
        self.app.route("/RVC_server_start",methods=["POST"])(self.RVC_server_start)
        self.app.route("/RVC_start",methods=["POST"])(self.RVC_start)
        self.app.route("/change_rvc_config",methods=["POST"])(self.change_rvc_config)
        self.app.route("/check_RVCserver_is_open")(self.check_RVCserver_is_open)
        self.app.route("/RVC_stop")(self.RVC_stop)

    async def index(self):
        """
        /,主页初始化
        """
        providers = self.tts_providers
        audio_devices = self.get_audio_devices()
        return await render_template('index.html',
                                    providers=providers,
                                    edge_tts_voices=self.Edge_TTS_voices,
                                    audio_devices=audio_devices,
                                    ali_tts_voices=list(self.ali_tts_voices.keys()),
                                    sambert_tts_voices=list(self.sambert_tts_voices.keys()),
                                    user_config = self.user_config,
                                    user_rvc_config = self.user_rvc_config,
                                    text_split_method = list(self.text_split_method.keys()),
                                    GPTmodel_list = list(self.scan_GPTmodel_list(self.GPTvts_modelPath)),
                                    SovitsMoedel_list = list(self.scan_SovitsModel_list(self.GPTvts_modelPath)),
                                    RVC_input_devices = list(self.get_input_devices()),
                                    RVC_output_devices = list(self.get_output_devices()),
                                    RVC_weights = list(self.scan_RVCweight_list(self.rvc_weights_path)),
                                    RVC_indexes = list(self.scan_RVCindex_list(self.rvc_index_path)),
                                    )
    """
    返回格式
     data = {
                "text":"要处理的文本",
                "device":"默认设备",
                "provider":"Edge TTS",
                "edge_tts_voice":"zh-CN-XiaoxiaoNeural",
                "ali_api_key":"sk-xxxxxxxxxxxxxxx",
                "ali_tts_voice":"龙婉-普通话-语音助手、导航播报、聊天数字人",
                "sambert_tts_voice":"知婧-严厉女声-通用场景",
                "GPTvts_character": "温迪",
                "GPTvts_emotion": "开心_happy",
                "GPTvts_sample": "【开心_happy】…凯亚是个不好应付的人啊，不过免费的酒真好喝。.wav"
                "GPTvts_speed_factor":1
                "GPTvts_temperature_factor":1
                "GPTvts_text_split_method":"按中文句号。切",
                "GPTmodelName":"",
                "SovitsModelName":"",
                "parallel_infer":True,
                "split_bucket":True,
                "batch_size_slider":5,
                "batch_threshold_slider":0.75,
                "isdownload":False,
                "isplayaudio":True,
                "isIndex_tts_flash":False
            };
    """
    async def tts_endpoint(self):
        """
        /tts,转换并播放文本
        """
        data = await request.get_json()
        if data is None:
            return jsonify({'error': '无效的JSON数据'}), 400
        config_to_save = {
            "provider":data.get("provider",self.user_config.get("provider")),
            "edge_tts_voice":data.get("edge_tts_voice",self.user_config.get("edge_tts_voice")),
            "device":data.get("device",self.user_config.get("device")),
            "ali_tts_voice":data.get("ali_tts_voice",self.user_config.get("ali_tts_voice")),
            "sambert_tts_voice":data.get("sambert_tts_voice",self.user_config.get("sambert_tts_voice")),
            "ali_api_key":data.get("ali_api_key",self.user_config.get("ali_api_key")),
            "GPTvts_character": data.get("GPTvts_character", "温迪"),
            "GPTvts_emotion": data.get("GPTvts_emotion", "开心_happy"),
            "GPTvts_sample": data.get("GPTvts_sample", ""),
            "GPTvts_speed_factor":data.get("GPTvts_speed_factor", 1.0),
            "GPTvts_temperature_factor":data.get("GPTvts_temperature_factor", 1.0),
            "GPTvts_text_split_method":data.get("GPTvts_text_split_method", "按中文句号。切"),
            "GPTmodelName":data.get("GPTmodelName", ""),
            "SovitsModelName":data.get("SovitsModelName", ""),
            "parallel_infer":bool(data.get("parallel_infer", True)),
            "split_bucket":bool(data.get("split_bucket", True)),
            "batch_size_slider":data.get("batch_size_slider", 5),
            "batch_threshold_slider":data.get("batch_threshold_slider", 0.75),
            "isdownload":bool(data.get('isdownload', False)),
            "isplayaudio":bool(data.get('isplayaudio', True)),
            "isIndex_tts_flash":bool(data.get("isIndex_tts_flash",False))
        }
        self.save_config(config_to_save)
        self.user_config = config_to_save
        text = data.get('text', '')
        device = data.get('device', '')
        self.set_audio_device(device)
        id = uuid.uuid4().hex
        isPlayAudio = bool(data.get('isplayaudio', True))
        isdownload = bool(data.get('isdownload', False))
        temp_file = self.savePath / f"save_voice_{id}.mp3"
        mimetype='audio/mp3'
        attachment_filename = "audio.mp3"
        if data.get("provider") == "GPTvts本地推理":
            temp_file = self.savePath / f"save_voice_{id}.wav"
            mimetype='audio/wav'
            attachment_filename = "audio.wav"
        try:
            self.osc_client.send_message("/chatbox/input", [text, True])
            print("已发送文本到VRChat OSC")
        except Exception as e:
            print(f"发送OSC消息失败: {e}")
        if data.get("provider") == "Edge TTS":
            if await self.use_edge_tts(data,temp_file):
                print(f"已转换文本: 生成临时文件{temp_file}")
            else:
                print("Edge TTS转换失败")
                return jsonify({'error': "tts转换失败"}), 400
        if data.get("provider") == "阿里百炼cosyvice":
            if await self.use_ali_tts(data,temp_file):
                print(f"已转使用阿里百炼换文本: 生成临时文件{temp_file}")
            else:
                print("阿里百炼转换失败")
                return jsonify({'error': "tts转换失败"}), 400
        if data.get("provider") == "阿里百炼sambert":
            if await self.use_sambert_tts(data,temp_file):
                print(f"已转使用阿里百炼sambert模型换文本: 生成临时文件{temp_file}")
            else:
                print("阿里百炼sambert模型转换失败")
                return jsonify({'error': "tts转换失败"}), 400
        if data.get("provider") == "GPTvts本地推理":
            if await self.use_GPTvts(data,temp_file):
                print(f"已转使用GPTvts换文本: 生成临时文件{temp_file}")
            else:
                print("GPTvts模型转换失败")
                return  jsonify({'error': "tts转换失败"}), 400
        if data.get("provider") == "Index TTS":
            if await self.use_index_tts(data,temp_file):
                print(f"已转使用Index TTS换文本: 生成临时文件{temp_file}")
            else:
                print("Index TTS转换失败")
                return jsonify({'error': "tts转换失败"}), 400
        with open(temp_file,'rb') as audio_file:
            audio_data = audio_file.read()
        response_data = None
        if isdownload:
            response_data = await send_file(
                io.BytesIO(audio_data),
                mimetype=mimetype,
                as_attachment=True,
                attachment_filename=attachment_filename
            )
        else:
            response_data = jsonify({
                "status":"success",
                "message": "tts转换成功",
                "audio_info":{
                    "size":len(audio_data),
                    "mimetype":mimetype,
                    "attachment_filename":attachment_filename
                }
            })
        if isPlayAudio:
            loop = asyncio.get_event_loop()
            async def play_and_cleanup():
                try:
                    if await self.play_audio(temp_file):
                        print(f"已播放音频文件: {temp_file}")
                    else:
                        print("播放音频文件失败")
                        return jsonify({'error': "音频播放失败"}), 400
                finally:
                    if hasattr(pygame.mixer, 'get_init') and pygame.mixer.get_init():
                        pygame.mixer.quit()
                    if os.path.exists(temp_file):
                        try:
                            os.remove(temp_file)
                            print(f"已清理临时文件: {temp_file}")
                        except Exception as e:
                            print(f"清理临时文件{temp_file}失败: {e}")
            loop.create_task(play_and_cleanup())
        else:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"已清理临时文件: {temp_file}")
                except Exception as e:
                    print(f"清理临时文件{temp_file}失败: {e}")
        return response_data
    async def GPTvts_tts_start(self):
        """
        /GPTvts_tts_start启动GPTvts本地推理服务
        """
        try:
            if self.local_tts_process is not None and self.local_tts_process.poll() is None:
                print("GPTvts本地推理服务已启动，将关闭GPTvts本地推理服务")
                self.cleanup()
                time.sleep(1)
                return jsonify({"status":"tts_close","message": "GPTvts本地推理服务已关闭"})
            self.output_queue = queue.Queue()
            self.local_tts_process = subprocess.Popen(
                [
                    self.local_interpreter_path,
                    self.local_script_path,
                    '-a', '127.0.0.1',
                    '-p', '9880',
                    '-c', 'GPT_SoVITS/configs/tts_infer.yaml'
                ],
                cwd=self.local_script_cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                text=True,
                #creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0,
            )
            stdout_thread = threading.Thread(target=self.read_output,args=(self.local_tts_process.stdout,self.output_queue))
            stderr_thread = threading.Thread(target=self.read_output,args=(self.local_tts_process.stderr,self.output_queue))
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()
            time.sleep(1)
            start_time = time.time()
            timout = 60
            while True:
                if self.local_tts_process.poll() is not None:
                    print(f"启动失败，进程返回码：{self.local_tts_process.poll()}")
                    return jsonify({"status":"error","message": f"启动失败，进程返回码：{self.local_tts_process.poll()}"})
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get("http://127.0.0.1:9880/")
                        response_data = response.json()
                        if response_data.get("detail") == "Not Found":
                            print(f"启动成功，进程返回码：{self.local_tts_process.poll()}")
                            return jsonify({"status":"tts_open","message": f"启动成功，进程返回码：{self.local_tts_process.poll()}"})
                except Exception:
                    print(f"等待启动中。。已等待{time.time() - start_time}秒")
                if time.time() - start_time > timout:
                    print(f"启动失败，进程返回码：{self.local_tts_process.poll()}")
                    return jsonify({"status":"error","message": f"启动失败，进程返回码：{self.local_tts_process.poll()}"})
                time.sleep(1)
        except Exception as e:
            print(f"启动本地TTS服务失败: {e}")
            self.local_tts_process = None
            return jsonify({"status":"error","message": f"启动本地TTS服务失败: {e}"})
        
    async def index_tts_start(self):
        """
        /index_tts_start启动Index TTS服务
        """
        if self.index_tts is None:
            try:
                checkpoint_path = self.index_path
                config_path = os.path.join(self.index_path,"config.yaml")
                self.index_tts = IndexTTS(model_dir=checkpoint_path,cfg_path=config_path)
            except Exception as e:
                print(f"启动Index TTS服务失败: {e}")
                return jsonify({"status":"error","message": f"启动Index TTS服务失败: {e}"})
            finally:
                print("Index TTS服务已启动")
                return jsonify({"status":"index_tts_open","message":"indextts启动成功"})

        else:
            try:
                print("indexTTS服务已经启动，将关闭")
                self.index_tts.torch_empty_cache()
                del self.index_tts
                self.index_tts = None
                torch.cuda.empty_cache()
                gc.collect()
            except Exception:
                print("index实例关闭失败")
                return jsonify({"status":"error"})
            finally:
                print("Index TTS服务关闭")
                return jsonify({"status":"index_tts_close"})
    async def RVC_server_start(self):
        """
        /RVC_server_start开始RVC实例
        """
        data = await request.get_json()
        value = {
            "pth_path":os.path.join(self.rvc_weights_path,data.get("pth_path")),
            "index_path":os.path.join(self.rvc_index_path,data.get("index_path")),
            "sg_input_device":data.get("sg_input_device"),
            "sg_output_device":data.get("sg_output_device"),
            "sg_hostapi":"",
            "wasapi_exclusive":False,
            "sr_type":"sr_device",
            "threhold":int(data.get("threhold")),
            "pitch":int(data.get("pitch")),
            "formant":float(data.get("formant")),
            "block_time":float(data.get("block_time")),
            "crossfade_length":float(data.get("crossfade_length")),
            "extra_time":float(data.get("extra_time")),
            "I_noise_reduce":bool(data.get("I_noise_reduce")),
            "O_noise_reduce":bool(data.get("O_noise_reduce")),
            "use_pv":bool(data.get("use_pv")),
            "rms_mix_rate":float(data.get("rms_mix_rate")),
            "index_rate":float(data.get("index_rate")),
            "n_cpu":int(data.get("n_cpu")),
            "f0method":str(data.get("f0method"))
        }
        if self.rvc_server is not None:
            self.rvc_server.stop_stream()
            del self.rvc_server
            self.rvc_server = None
            torch.cuda.empty_cache()
            print("RVC实例已关闭")
            return jsonify({"status":"OK","message": "RVC实例已关闭","code":200})
        else:
            try:
                #freeze_support()
                from gui_v1 import create_audio_api
                self.rvc_server = create_audio_api()
                if await self.RVC_config(value):
                    print("参数初始化完毕")
            except Exception as e:
                print(f"Start conversion error: {e}")
                return jsonify({"status":"error","message": f"启动语音转换失败: {e}"})
            finally:
                print("RVC实例已启动")
                return jsonify({"status":"OK","message": "语音转换已启动","code":200})
    async def RVC_start(self):
        """
        /RVC_start启动转换
        """
        data = await request.get_json()
        value = {
            "pth_path":os.path.join(self.rvc_weights_path,data.get("pth_path")),
            "index_path":os.path.join(self.rvc_index_path,data.get("index_path")),
            "sg_input_device":data.get("sg_input_device"),
            "sg_output_device":data.get("sg_output_device"),
            "sg_hostapi":"",
            "wasapi_exclusive":False,
            "sr_type":"sr_device",
            "threhold":int(data.get("threhold")),
            "pitch":int(data.get("pitch")),
            "formant":float(data.get("formant")),
            "block_time":float(data.get("block_time")),
            "crossfade_length":float(data.get("crossfade_length")),
            "extra_time":float(data.get("extra_time")),
            "I_noise_reduce":bool(data.get("I_noise_reduce")),
            "O_noise_reduce":bool(data.get("O_noise_reduce")),
            "use_pv":bool(data.get("use_pv")),
            "rms_mix_rate":float(data.get("rms_mix_rate")),
            "index_rate":float(data.get("index_rate")),
            "n_cpu":int(data.get("n_cpu")),
            "f0method":str(data.get("f0method"))
        }
        if self.rvc_server is not None:
            try:
                if await self.RVC_config(value):
                    self.rvc_server.start_vc()
                    if self.rvc_server.stream is not None:
                        self.rvc_server.delay_time = (
                            self.rvc_server.stream.latency[-1]
                            + value["block_time"]
                            + value["crossfade_length"]
                            + 0.01
                        )
                    if value["I_noise_reduce"]:
                        self.rvc_server.delay_time += min(value["crossfade_length"], 0.04)
                    self.rvc_server.start_stream()
            except Exception as e:
                print(f"启动语音转换失败: {e}")
                return jsonify({"status":"error","message": f"启动语音转换失败: {e}"})
            finally:
                return jsonify({"status":"OK","message": "语音转换已启动","code":200})
        else:
            print("请先启动RVC实例")
            return jsonify({"status":"error","message": "请先启动RVC实例"})
    async def RVC_stop(self):
        """
        /RVC_stop停止转换
        """
        if self.rvc_server is not None:
            try:
                self.rvc_server.stop_stream()
            except Exception as e:
                print(f"停止语音转换失败: {e}")
                return jsonify({"status":"error","message": f"停止语音转换失败: {e}"})
            finally:
                return jsonify({"status":"OK","message": "语音转换已停止","code":200})
        else:
            print("请先启动RVC实例")
            return jsonify({"status":"error","message": "请先启动RVC实例"})

    async def change_rvc_config(self,value = None):
        """
        /change_rvc_config修改RVC参数
        """
        data = await request.get_json()
        value = {
            "pth_path":os.path.join(self.rvc_weights_path,data.get("pth_path")),
            "index_path":os.path.join(self.rvc_index_path,data.get("index_path")),
            "sg_input_device":data.get("sg_input_device"),
            "sg_output_device":data.get("sg_output_device"),
            "sg_hostapi":"",
            "wasapi_exclusive":False,
            "sr_type":"sr_device",
            "threhold":int(data.get("threhold")),
            "pitch":int(data.get("pitch")),
            "formant":float(data.get("formant")),
            "block_time":float(data.get("block_time")),
            "crossfade_length":float(data.get("crossfade_length")),
            "extra_time":float(data.get("extra_time")),
            "I_noise_reduce":bool(data.get("I_noise_reduce")),
            "O_noise_reduce":bool(data.get("O_noise_reduce")),
            "use_pv":bool(data.get("use_pv")),
            "rms_mix_rate":float(data.get("rms_mix_rate")),
            "index_rate":float(data.get("index_rate")),
            "n_cpu":int(data.get("n_cpu")),
            "f0method":str(data.get("f0method"))
        }
        if self.rvc_server is not None:
            self.rvc_server.gui_config.threhold = value["threhold"]
            self.rvc_server.gui_config.pitch = value["pitch"]
            self.rvc_server.gui_config.formant = value["formant"]
            self.rvc_server.gui_config.index_rate = value["index_rate"]
            self.rvc_server.gui_config.rms_mix_rate = value["rms_mix_rate"]
            self.rvc_server.gui_config.f0method = value["f0method"]
            self.rvc_server.gui_config.I_noise_reduce = value["I_noise_reduce"]
            self.rvc_server.gui_config.O_noise_reduce = value["O_noise_reduce"]
            self.rvc_server.gui_config.use_pv = value["use_pv"]
            if hasattr(self.rvc_server,"rvc"):
                self.rvc_server.rvc.change_key(value["pitch"])
            if hasattr(self.rvc_server,"rvc"):
                self.rvc_server.rvc.change_formant(value["formant"])
            if hasattr(self.rvc_server,"rvc"):
                self.rvc_server.rvc.change_index_rate(value["index_rate"])
            if self.rvc_server.stream is not None:
                        self.rvc_server.delay_time += (
                            1 if value["I_noise_reduce"] else -1
                        ) * min(value["crossfade_length"], 0.04)
        else:
            return jsonify({"status":"error","message": "请先启动RVC实例"})

    async def RVC_config(self,config_data):
        """
        /RVC_config设置RVC参数
        """
        try:
            if self.rvc_server.set_values(config_data):
                with open("configs/config.json", "w", encoding='utf-8') as j:
                    json.dump(config_data, j, ensure_ascii=False)
                print("配置设置成功")
                return True
        except Exception as e:
            print("配置设置失败:")
            return False
    async def check_RVCserver_is_open(self):
        """
        /check_RVCserver_is_open检查RVC本地推理服务是否已启动
        """
        if self.rvc_server is None:
            return jsonify({"status":"rvc_close","message": "RVC本地推理服务未启动"})
        elif self.rvc_server is not None:
            return jsonify({"status":"rvc_open","message": "RVC本地推理服务已启动"})
        else:
            return jsonify({"status":"error","message": "检查RVC服务是否已启动失败"})
    async def check_GPTvts_is_open(self):
        """
        /check_GPTvts_is_open检查GPTvts本地推理服务是否已启动
        """
        if self.local_tts_process is None or self.local_tts_process.poll() is not None:
            return jsonify({"status":"tts_close","message": "GPTvts本地推理服务未启动"})
        elif self.local_tts_process is not None and self.local_tts_process.poll() is None:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get("http://127.0.0.1:9880/")
                    response_data = response.json()
                if response_data.get("detail") == "Not Found":
                    return jsonify({"status":"tts_open","message": "GPTvts本地推理服务已启动"})
            except Exception as e:
                print(f"GPTvts可能正在启动中: {e}")
                return jsonify({"status":"error","message": f"检查本地TTS服务是否已启动失败: {e}"})
        else:
            return jsonify({"status":"error","message": "检查本地TTS服务是否已启动失败"})
    async def check_index_tts(self):
        """
        /check_index_tts检查index服务的启动状态
        """
        if self.index_tts is None:
            return jsonify({"status":"index_tts_isClose"})
        elif self.index_tts is not None:
            return jsonify({"status":"index_tts_isOpen"})
        else:
            return jsonify({"status":"error"})
    async def selectModel(self):
        """
        /selectModel切换GPTvts模型
        """
        data =await request.get_json()
        GPTmodelName = data.get("GPTmodelName", "")
        SovitsModelName= data.get("SovitsModelName", "")
        if GPTmodelName is not None:
            path = os.path.join(self.GPTvts_modelPath, GPTmodelName)
            url1 = f"http://127.0.0.1:9880/set_gpt_weights?weights_path={path}"
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url1)
                    response_data = response.json()
                except Exception:
                    return jsonify({"status":"error","message": "本地推理服务没有启动"})
                if response_data.get("code") == 400:
                    return jsonify({"status":"error","message": "模型不存在"})
        if SovitsModelName is not None:
            path2 = os.path.join(self.GPTvts_modelPath, SovitsModelName)
            url2 = f"http://127.0.0.1:9880/set_sovits_weights?weights_path={path2}"
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url2)
                    response_data2 = response.json()
                except Exception:
                    return jsonify({"status":"error","message": "本地推理服务没有启动"})
                if response_data.get("code") == 400:
                    return jsonify({"status":"error","message": "模型不存在"})
        return jsonify({"status":"success","message": "选择模型成功","GPTmodel":response_data,"SovitsModel":response_data2})
    async def get_voice_list(self):
        """
        /get_voice_list获取GPTvts语音音频列表
        """
        voice_list = self.scan_voice_folders(self.GPTvts_voices_path)
        return jsonify(voice_list)
    async def play_audio(self, audio_file):
        """
        播放音频文件
        """
        try:
            pygame.mixer.init(devicename=self.current_device)
            print(f"已设置音频设备: {self.current_device}")
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                # pygame.time.Clock().tick(10)
            pygame.mixer.quit()
            return True
        except Exception as e:
            print(f"播放音频文件失败: {e}")
            return False
    async def use_edge_tts(self,data,temp_file):
        """
        使用Edge TTS服务转换文本
        """
        try:
            communicate = edge_tts.Communicate(data.get("text",""), data.get("edge_tts_voice",""))
            await communicate.save(temp_file)
            return True
        except Exception as e:
            print(f"Edge TTS转换失败: {e}")
            return False
    async def use_ali_tts(self,data,temp_file):
        """
        使用阿里百炼服务转换文本
        """
        model = "cosyvoice-v1"
        voice = self.ali_tts_voices.get(data.get("ali_tts_voice",""))
        try:
            if data.get("ali_api_key") == "":
                print("阿里百炼API密钥为空")
                return False
            dashscope.api_key = data.get("ali_api_key","")
        except dashscope.DashScopeError as e:
            print(f"阿里百炼转换失败: {e}")
            return False
        try:
            synthesizer = SpeechSynthesizerV2(model=model, voice=voice)
            audio = synthesizer.call(data.get("text",""))
        except Exception as e:
            print(f"阿里百炼转换失败: {e}")
            return False
        with open(temp_file, 'wb') as f:
            f.write(audio)
        return True
    async def use_sambert_tts(self,data,file_path):
        """
        使用阿里百炼sambert模型服务转换文本
        """
        model = self.sambert_tts_voices.get(data.get("sambert_tts_voice"))
        print("使用阿里百炼sambert模型服务转换文本，当前模型为"+model)
        key = data.get("ali_api_key","")
        text = str(data.get("text",""))
        try:
            if data.get("ali_api_key") == "":
                print("阿里百炼API密钥为空")
                return False
            dashscope.api_key = key
            result = SpeechSynthesizerV1.call(model=model,text=text,sample_rate=48000,format='mp3')
        except Exception as e:
            print(f"阿里百炼转换失败: {e}")
            return False
        if result.get_audio_data() is not None:
            with open(file_path, 'wb') as f:
                f.write(result.get_audio_data())
            return True
        else:
            print("阿里百炼转换失败")
            return False
    async def use_GPTvts(self,data,temp_file):
        """
        使用GPTvts模型服务转换文本
        """

        url = "http://127.0.0.1:9880/tts"
        ref_audio_path = os.path.join(self.GPTvts_voices_path, data.get("GPTvts_character"),data.get("GPTvts_emotion"),data.get("GPTvts_sample"))
        ref_audio = data.get("GPTvts_sample")
        start_index = ref_audio.find("】")+1
        end_index = ref_audio.find(".wav")
        text_split_method = self.text_split_method.get(data.get("GPTvts_text_split_method","按中文句号。切"))
        extracted_text = ref_audio[start_index:end_index]
        print("使用GPTvts模型服务转换文本，当前模型为"+ref_audio_path)
        json = {
            "text": data.get("text",""),
            "text_lang": "zh",
            "ref_audio_path": ref_audio_path,
            "aux_ref_audio_paths": [],
            "prompt_text": extracted_text,
            "prompt_lang": "zh",
            "top_k":5,
            "top_p":1,
            "temperature":float(data.get("GPTvts_temperature_factor",1)),
            "text_split_method":text_split_method,
            "batch_size": int(data.get("batch_size_slider",5)),
            "batch_threshold": float(data.get("batch_threshold_slider",0.75)),
            "split_bucket": bool(data.get("split_bucket",True)),
            "speed_factor":float(data.get("GPTvts_speed_factor",1)),
            "streaming_mode": False,
            "seed": -1,
            "parallel_infer": bool(data.get("parallel_infer",True)),
            "repetition_penalty": 1.35,
            "sample_steps": 32,
            "super_sampling": False
            }
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            try:
                print(f"正在请求GPTvts服务{json}")
                response = await client.post(url, json=json, headers=headers,timeout=120)
            except Exception as e:
                print(f"请求GPTvts服务失败: {e}")
                return False
            if response.status_code == 200:
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                return True
    async def use_index_tts(self,data,temp_file):
        """
        使用index服务转换文本
        """
        if self.index_tts is None:
            print("indexTTS服务未启动")
            return False
        voice = os.path.join(self.GPTvts_voices_path, data.get("GPTvts_character"),data.get("GPTvts_emotion"),data.get("GPTvts_sample"))
        text= data.get("text","")
        isFlash = bool(data.get("isIndex_tts_flash","False"))
        if isFlash:
            self.index_tts.infer_fast(voice,text,temp_file)
        else:
            self.index_tts.infer(voice, text, temp_file)
        return True
    def get_audio_devices(self):
        """
        扫描系统音频输出设备
        """
        devices = {"默认设备": "default"}
        sapi = win32com.client.Dispatch("SAPI.SpVoice")
        audio_outputs = sapi.GetAudioOutputs()  
        for i in range(audio_outputs.Count):
            device_desc = audio_outputs.Item(i).GetDescription()#
            devices[device_desc] = i  
        print(f"已找到 {audio_outputs.Count} 个音频设备")
        print(f"已找到 {str(devices)} 个音频设备")
        return devices
    def update_devices(self, hostapi_name=None):
        """获取设备列表"""
        sd._terminate()
        sd._initialize()
        devices = sd.query_devices()
        hostapis = sd.query_hostapis()
        for hostapi in hostapis:
            for device_idx in hostapi["devices"]:
                devices[device_idx]["hostapi_name"] = hostapi["name"]
        a = [hostapi["name"] for hostapi in hostapis]
        if hostapi_name not in a:
            hostapi_name = a[0]
        input_devices = [
            d["name"]
            for d in devices
            if d["max_input_channels"] > 0 and d["hostapi_name"] == hostapi_name
        ]
        output_devices = [
            d["name"]
            for d in devices
            if d["max_output_channels"] > 0 and d["hostapi_name"] == hostapi_name
        ]
        input_devices_indices = [
            d["index"] if "index" in d else d["name"]
            for d in devices
            if d["max_input_channels"] > 0 and d["hostapi_name"] == hostapi_name
        ]
        output_devices_indices = [
            d["index"] if "index" in d else d["name"]
            for d in devices
            if d["max_output_channels"] > 0 and d["hostapi_name"] == hostapi_name
        ]
        return(
            input_devices,
            output_devices,
            input_devices_indices,
            output_devices_indices,
        )
    def get_input_devices(self):
        try:
            input_devices,_, _, _ = self.update_devices()
            return input_devices
        except Exception as e:
            print(f"Failed to get output devices: {e}")

    def get_output_devices(self):
        try:
            _, output_devices, _, _ = self.update_devices()
            return output_devices
        except Exception as e:
            print(f"Failed to get output devices: {e}")
    def set_audio_device(self, device):
        """
        设置音频输出设备
        """
        self.current_device = device
    def read_output(self, pipe, output_queue):
        try:
            while True:
                line = pipe.readline()
                if not line:
                    break
                if isinstance(line, bytes):
                    line = line.decode('utf-8', errors='replace')
                line = line.strip()
                print(print(f"[进程输出] {line}"))
                output_queue.put(line)
        except Exception as e:
            print(f"读取输出时发生错误: {e}")
        finally:
            pipe.close()
    def scan_GPTmodel_list(self,path):
        """
        扫描模型文件
        """
        model_path = path
        model_list = []
        try:
            for model in model_path.iterdir():
                if model.name.endswith(".pth"):# 检查文件是否为.pth格式
                     model_list.append(model.name)
            return model_list
        except Exception:
            return model_list
    def scan_RVCweight_list(self,path):
        """
        扫描模型文件
        """
        model_path = path
        model_list = []
        try:
            for model in model_path.iterdir():
                if model.name.endswith(".pth"):# 检查文件是否为.pth格式
                     model_list.append(model.name)
            return model_list
        except Exception:
            return model_list
    def scan_RVCindex_list(self,path):
        """
        扫描模型文件
        """
        model_path = path
        model_list = []
        for model in model_path.iterdir():
            if model.name.endswith(".index"):# 检查文件是否为.pth格式
                model_list.append(model.name)
        return model_list
    def scan_SovitsModel_list(self,path):
        """
        扫描模型文件
        """
        model_path = path
        model_list = []
        try:
            for model in model_path.iterdir():
                if model.name.endswith(".pth"):# 检查文件是否为.pth格式
                     model_list.append(model.name)
            return model_list
        except Exception:
            return model_list
    def scan_voice_folders(self,path):
        """
        扫描语音文件夹
        """
        voices_path = path
        voices_list = []
        for character_dir in voices_path.iterdir():
            if character_dir.is_dir():
                character_name = character_dir.name
                emotions = []
            
            # 遍历第二层目录（情感文件夹）
            for emotion_dir in character_dir.iterdir():
                if emotion_dir.is_dir():
                    emotion_name = emotion_dir.name
                    # 获取情感文件夹中的音频文件
                    audio_files = [f.name for f in emotion_dir.iterdir() if f.suffix.lower() in ('.wav', '.mp3')]
                    if audio_files:
                        emotions.append({
                            "emotion": emotion_name,
                            "samples": audio_files
                        })
            if emotions:
                voices_list.append({
                    "character": character_name,
                    "emotions": emotions
                })
        return voices_list
    def cleanup(self):
        """
        清理
        """
        if self.local_tts_process is not None:
            try:
                if os.name == 'nt':
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.local_tts_process.pid)],stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                else:
                    self.local_tts_process.terminate()
                self.local_tts_process.wait(timeout=5)
            except Exception as e:
                print(f"清理本地TTS服务失败: {e}")
                self.local_tts_process.kill()
            finally:
                self.local_tts_process = None
    '''
    def run(self,host,port,certfile, keyfile):
        try:
            self.app.run(host=host,port=port,certfile=certfile, keyfile=keyfile)
        finally:
            self.cleanup()
    '''
    def run(self,host,port):
        try:
            self.app.run(host=host,port=port)
        finally:
            self.cleanup()
if __name__ == '__main__': 
    host = os.environ.get('APP_HOST', '0.0.0.0') # 默认绑定到所有接口
    port = int(os.environ.get('APP_PORT', 1145)) # 默认端口 1145
    app = TTSWebApp()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) # 连接到一个外部地址以获取本机IP
        local_ip = s.getsockname()[0]
        s.close()
        print(f"本机局域网 IP 地址: {local_ip}:{port}")
    except Exception as e:
        print(f"无法获取本机局域网 IP 地址: {e}")
        local_ip = "未知"

    print(f"正在启动应用，监听地址: {host}:{port}")
    print("""
        ███╗   ██╗  ██╗  ███████╗  ████████╗  ████████╗  ███████╗
        ████╗  ██║  ██║  ██╔════╝  ╚══██╔══╝  ╚══██╔══╝  ██╔════╝
        ██╔██╗ ██║  ██║  █████╗       ██║        ██║     ███████╗
        ██║╚██╗██║  ██║  ██╔══╝       ██║        ██║     ╚════██║
        ██║ ╚████║  ██║  ███████╗     ██║        ██║     ███████║
        ╚═╝  ╚═══╝  ╚═╝  ╚══════╝     ╚═╝        ╚═╝     ╚══════╝
        """)
    try:
        '''
        app.run(host=host, 
                port=port,
                certfile='cert.pem',
                keyfile='key.pem'
                )
        '''
        app.run(host=host, port=port)
    except Exception as e:
        print(f"启动应用时发生错误: {e}")
        print("请检查端口是否被占用，或者使用不同的端口启动应用。")
        input("按 Enter 键退出...")
