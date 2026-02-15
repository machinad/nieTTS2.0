from quart import Quart,render_template,request,jsonify,send_file
import os
import win32com.client
import edge_tts
import uuid
import pygame
import json
import io
import subprocess
import socket
import atexit
import asyncio
# import ssl  # 暂时注释掉，因为实际使用openssl命令行
import tempfile
from pythonosc import udp_client
from pathlib import Path
import dashscope
import webbrowser
from openai import OpenAI
from dashscope.audio.tts_v2 import SpeechSynthesizer as SpeechSynthesizerV2
from dashscope.audio.tts import SpeechSynthesizer as SpeechSynthesizerV1
class TTSWebApp:
    def __init__(self):
        self.Edge_TTS_voices = {
            "汉语女声-晓晓-新闻小说-温柔":"zh-CN-XiaoxiaoNeural",
            "汉语女声-晓艺-漫画小说-活泼":"zh-CN-XiaoyiNeural",
            "汉语女声-晓贝-辽宁方言-幽默":"zh-CN-liaoning-XiaobeiNeural",
            "汉语女声-晓倪-西安方言-明亮":"zh-CN-shaanxi-XiaoniNeural",
            "汉语男声-云间-体育小说-激情":"zh-CN-YunjianNeural",
            "汉语男声-云曦-小说-活泼阳光":"zh-CN-YunxiNeural",
            "汉语男声-云霞-漫画小说-可爱":"zh-CN-YunxiaNeural",
            "汉语男声-云阳-新闻-专业可靠":"zh-CN-YunyangNeural",
            "台湾女声-晓晨-普通-阳光积极":"zh-TW-HsiaoChenNeural",
            "台湾女声-晓玉-普通-阳光积极":"zh-TW-HsiaoYuNeural",
            "台湾男声-云杰-普通-阳光积极":"zh-TW-YunJheNeural",
            "粤语女声-晓佳-普通-阳光积极":"zh-HK-HiuGaaiNeural",
            "粤语女声-晓雯-普通-阳光积极":"zh-HK-HiuMaanNeural",
            "粤语男声-云龙-普通-阳光积极":"zh-HK-WanLungNeural",
            "日语男声-圭太-普通-阳光积极":"ja-JP-KeitaNeural",
            "日语女声-七海-普通-阳光积极":"ja-JP-NanamiNeural"
        }
        self.tlanguages = [
            "英语",
            "日语"
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
        self.local_tts_process = None
        self.savePath = Path("./save").resolve()
        try:
            self.savePath.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"创建目录{self.savePath}失败: {e}")
        self.user_config = self.load_config()
        #self.user_rvc_config = self.load_rvc_config()
        self.app = Quart(__name__)
        self.current_device = "default"
        self.tts_providers = [
            "Edge TTS",
            "阿里百炼cosyvice",
            "阿里百炼sambert"
        ]
        
        self.setup_routes()
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
            "siliconflowApiKey":"",
            "tLanguage":"英语",
            "isdownload":False,
            "isplayaudio":True,
            "isTranslate":True,
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

    async def index(self):
        """
        /,主页初始化
        """
        providers = self.tts_providers
        audio_devices = self.get_audio_devices()
        return await render_template('index.html',
                                    providers=providers,
                                    edge_tts_voices=list(self.Edge_TTS_voices.keys()),
                                    audio_devices=audio_devices,
                                    tlanguages=self.tlanguages,
                                    ali_tts_voices=list(self.ali_tts_voices.keys()),
                                    sambert_tts_voices=list(self.sambert_tts_voices.keys()),
                                    user_config = self.user_config
                                    )
    async def useTranslate(self,text,tLanguage,apikey):
        url = "https://api.siliconflow.cn/v1"
        def call_api():
            client = OpenAI(
                api_key=apikey,
                base_url=url
            )
            try:
                response = client.chat.completions.create(
                    model = "Qwen/Qwen3-8B",
                    messages=[
                        {"role": "system", "content": f"你是一个专业的翻译家，你的任务是将用户提供的文本翻译成{tLanguage}，请确保翻译内容准确且符合目标语言的表达习惯。记住你只需要提供翻译内容，不需要任何额外的解释或评论。也不要回答任何问题，只需专注于翻译任务。你只能输出翻译后的文本，不允许有任何多余的内容。"},
                        {"role": "user", "content": f"{text}"}
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"调用翻译接口失败: {e}")
                return f"调用翻译接口失败: {e}"
        text = await asyncio.to_thread(call_api)
        print(f"翻译结果: {text}")
        return text
    
    async def tts_endpoint(self):
        """
        /tts,转换并播放文本
        """
        data = await request.get_json()
        if data is None:
            return jsonify({'error': '无效的JSON数据'}), 400

        # 输入验证
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': '文本内容不能为空'}), 400
        if len(text) > 5000:  # 限制文本长度
            return jsonify({'error': '文本内容过长，最多5000字符'}), 400

        provider = data.get("provider")
        valid_providers = ["Edge TTS", "阿里百炼cosyvice", "阿里百炼sambert"]
        if provider not in valid_providers:
            return jsonify({'error': f'无效的TTS引擎，支持: {", ".join(valid_providers)}'}), 400

        # 验证API密钥格式（如果提供）
        ali_api_key = data.get('ali_api_key', '')
        if provider in ["阿里百炼cosyvice", "阿里百炼sambert"] and not ali_api_key:
            return jsonify({'error': '阿里百炼API密钥不能为空'}), 400
        if ali_api_key and len(ali_api_key) < 10:  # 简单格式检查
            return jsonify({'error': 'API密钥格式无效'}), 400

        siliconflow_api_key = data.get('siliconflowApiKey', '')
        if data.get('isTranslate', False) and not siliconflow_api_key:
            return jsonify({'error': '翻译功能需要API密钥'}), 400
        config_to_save = {
            "provider":data.get("provider",self.user_config.get("provider")),
            "edge_tts_voice":data.get("edge_tts_voice",self.user_config.get("edge_tts_voice")),
            "device":data.get("device",self.user_config.get("device")),
            "ali_tts_voice":data.get("ali_tts_voice",self.user_config.get("ali_tts_voice")),
            "sambert_tts_voice":data.get("sambert_tts_voice",self.user_config.get("sambert_tts_voice")),
            "ali_api_key":data.get("ali_api_key",self.user_config.get("ali_api_key")),
            "siliconflowApiKey":data.get("siliconflowApiKey",self.user_config.get("siliconflowApiKey")),
            "tLanguage":data.get("tLanguage",self.user_config.get("tLanguage")),
            "isdownload":bool(data.get('isdownload', False)),
            "isplayaudio":bool(data.get('isplayaudio', True)),
            "isTranslate":bool(data.get("isTranslate",True)),
            "isIndex_tts_flash":bool(data.get("isIndex_tts_flash",False))
        }
        self.save_config(config_to_save)
        self.user_config = config_to_save
        device = data.get('device', '')
        self.set_audio_device(device)
        id = uuid.uuid4().hex
        isPlayAudio = bool(data.get('isplayaudio', True))
        isdownload = bool(data.get('isdownload', False))
        temp_file = self.savePath / f"save_voice_{id}.mp3"
        # 定义清理临时文件函数
        def remove_file(path):
            if os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"已清理临时文件: {path}")
                except Exception as e:
                    print(f"清理临时文件失败: {e}")
        mimetype='audio/mp3'
        attachment_filename = "audio.mp3"

        #判断是否翻译并且发送OSC消息
        if(data.get("isTranslate",False)):
            async def translate_and_send():
                t = await self.useTranslate(text,data.get("tLanguage"),data.get("siliconflowApiKey"))
                outText = text + ("\n" + t if t else "")
                try:
                    self.osc_client.send_message("/chatbox/input", [outText, True])
                    print("已发送文本到VRChat OSC")
                except Exception as e:
                    print(f"发送OSC消息失败: {e}")
            asyncio.create_task(translate_and_send())
        else:
            try:
                self.osc_client.send_message("/chatbox/input", [text, True])
                print("已发送文本到VRChat OSC")
            except Exception as e:
                print(f"发送OSC消息失败: {e}")
                
        #选择TTS引擎进行转换
        tts_success = False

        if provider == "Edge TTS":
            print("使用Edge TTS转换文本")
            if await self.use_edge_tts(data,temp_file):
                print(f"已转换文本: 生成临时文件{temp_file}")
                tts_success = True
            else:
                print("Edge TTS转换失败")
                remove_file(temp_file)
                return jsonify({'error': "tts转换失败"}), 400
        elif provider == "阿里百炼cosyvice":
            if await self.use_ali_tts(data,temp_file):
                print(f"已转使用阿里百炼换文本: 生成临时文件{temp_file}")
                tts_success = True
            else:
                print("阿里百炼转换失败")
                remove_file(temp_file)
                return jsonify({'error': "tts转换失败"}), 400
        elif provider == "阿里百炼sambert":
            if await self.use_sambert_tts(data,temp_file):
                print(f"已转使用阿里百炼sambert模型换文本: 生成临时文件{temp_file}")
                tts_success = True
            else:
                print("阿里百炼sambert模型转换失败")
                remove_file(temp_file)
                return jsonify({'error': "tts转换失败"}), 400
        else:
            print(f"无效的TTS引擎: {provider}")
            return jsonify({'error': f"无效的TTS引擎: {provider}"}), 400

        #检查音频文件是否生成成功
        if not tts_success or not os.path.exists(temp_file):
            print(f"TTS转换失败，未生成音频文件: {temp_file}")
            remove_file(temp_file)
            return jsonify({'error': "TTS转换失败，未生成音频文件"}), 400

        #读取生成的音频文件
        with open(temp_file,'rb') as audio_file:
            audio_data = audio_file.read()
        response_data = None
        #根据是否下载返回不同响应
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
        #播放音频并清理临时文件
        if isPlayAudio:
            loop = asyncio.get_event_loop()
            async def play_and_cleanup():
                try:
                    if await self.play_audio(temp_file):
                        print(f"已播放音频文件: {temp_file}")
                    else:
                        print("播放音频文件失败")
                        remove_file(temp_file)
                finally:
                    if hasattr(pygame.mixer, 'get_init') and pygame.mixer.get_init():
                        pygame.mixer.quit()
                    remove_file(temp_file)
            loop.create_task(play_and_cleanup())
        else:
            remove_file(temp_file)
        return response_data

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
            edge_tts_voice = self.Edge_TTS_voices.get(data.get("edge_tts_voice","zh-CN-XiaoxiaoNeural"))
            communicate = edge_tts.Communicate(data.get("text",""), edge_tts_voice)
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
   
    def set_audio_device(self, device):
        """
        设置音频输出设备
        """
        self.current_device = device
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
    def generate_self_signed_cert(self, ip_address, cert_path, key_path):
        """
        生成自签名证书
        """
        try:
            # 创建临时目录用于生成证书
            temp_dir = tempfile.mkdtemp()
            cert_file = os.path.join(temp_dir, "cert.pem")
            key_file = os.path.join(temp_dir, "key.pem")

            # 这部分代码实际上不会执行，只是为了消除IDE警告
            # 真正的证书生成是通过openssl命令行完成的

            # 使用openssl命令行生成证书（更可靠的方法）
            # 生成私钥
            subprocess.run([
                "openssl", "genrsa", "-out", key_file, "2048"
            ], check=True, capture_output=True)

            # 创建证书请求配置文件
            config_file = os.path.join(temp_dir, "cert.conf")
            with open(config_file, "w") as f:
                f.write(f"""[req]
                        default_bits = 2048
                        prompt = no
                        default_md = sha256
                        x509_extensions = v3_req
                        distinguished_name = dn

                        [dn]
                        C = CN
                        ST = Some-State
                        L = Some-City
                        O = nieTTS
                        OU = Development
                        CN = {ip_address}

                        [v3_req]
                        subjectAltName = @alt_names

                        [alt_names]
                        IP.1 = {ip_address}
                        DNS.1 = localhost
                        """)

            # 生成自签名证书
            subprocess.run([
                "openssl", "req", "-new", "-x509", "-nodes",
                "-days", "365", "-config", config_file,
                "-key", key_file, "-out", cert_file
            ], check=True, capture_output=True)

            # 复制到指定路径
            import shutil
            shutil.copy(cert_file, cert_path)
            shutil.copy(key_file, key_path)

            # 清理临时目录
            shutil.rmtree(temp_dir)

            print(f"已生成自签名证书: {cert_path}")
            print(f"已生成私钥: {key_path}")
            return True

        except Exception as e:
            print(f"生成自签名证书失败: {e}")
            print("请确保系统已安装OpenSSL")
            return False

    def cleanup_certificates(self, cert_path, key_path):
        """
        清理证书文件
        """
        try:
            if os.path.exists(cert_path):
                os.remove(cert_path)
                print(f"已清理证书文件: {cert_path}")
            if os.path.exists(key_path):
                os.remove(key_path)
                print(f"已清理私钥文件: {key_path}")
        except Exception as e:
            print(f"清理证书文件失败: {e}")

    def run(self, host, port, use_https=False, cert_path=None, key_path=None):
        """
        运行应用，支持HTTPS
        """
        try:
            if use_https and cert_path and key_path:
                if os.path.exists(cert_path) and os.path.exists(key_path):
                    self.app.run(host=host, port=port, certfile=cert_path, keyfile=key_path)
                else:
                    print(f"证书文件不存在，使用HTTP模式")
                    self.app.run(host=host, port=port)
            else:
                self.app.run(host=host, port=port)
        finally:
            self.cleanup()
if __name__ == '__main__':
    print("""
        ███╗   ██╗  ██╗  ███████╗  ████████╗  ████████╗  ███████╗
        ████╗  ██║  ██║  ██╔════╝  ╚══██╔══╝  ╚══██╔══╝  ██╔════╝
        ██╔██╗ ██║  ██║  █████╗       ██║        ██║     ███████╗
        ██║╚██╗██║  ██║  ██╔══╝       ██║        ██║     ╚════██║
        ██║ ╚████║  ██║  ███████╗     ██║        ██║     ███████║
        ╚═╝  ╚═══╝  ╚═╝  ╚══════╝     ╚═╝        ╚═╝     ╚══════╝
        """)
    host = os.environ.get('APP_HOST', '0.0.0.0') # 默认绑定到所有接口
    port = int(os.environ.get('APP_PORT', 1145)) # 默认端口 1145
    app = TTSWebApp()

    # 证书文件路径
    cert_dir = Path("./certificates")
    cert_dir.mkdir(exist_ok=True)
    cert_path = cert_dir / "cert.pem"
    key_path = cert_dir / "key.pem"

    local_ip = "未知"
    use_https = False

    try:
        # 获取本机IP地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) # 连接到一个外部地址以获取本机IP
        local_ip = s.getsockname()[0]
        s.close()

        # 生成自签名证书
        print(f"检测到本机IP地址: {local_ip}")
        print("正在生成自签名证书...")

        if app.generate_self_signed_cert(local_ip, str(cert_path), str(key_path)):
            use_https = True
            url = f"https://{local_ip}:{port}"
            print(f"""
                  =======================================================

                  已经启动HTTPS服务器，使用自签名证书保护通信安全
                  本机局域网 HTTPS 地址: {url}

                  ***可以使用任意同局域网设备访问此地址以打开前端页面***

                  注意: 由于使用自签名证书，浏览器会显示安全警告，请点击'高级'->'继续访问'

                  =======================================================
                  """
                  )
        else:
            url = f"http://{local_ip}:{port}"
            print(f"证书生成失败，使用HTTP模式")
            print(f"本机局域网 HTTP 地址: {url},可以使用任意同局域网设备访问此地址以打开前端页面")
            print("注意: HTTP模式下无法使用录音功能")

        # 打开浏览器
        if use_https:
            webbrowser.open(url)
        else:
            webbrowser.open(f"http://127.0.0.1:{port}")

    except Exception as e:
        print(f"无法获取本机局域网 IP 地址或生成证书: {e}")
        url = f"http://{host}:{port}"
        print(f"使用HTTP模式，监听地址: {url}")
        webbrowser.open(f"http://127.0.0.1:{port}")

    print(f"正在启动应用，监听地址: {host}:{port}")
    try:
        if use_https:
            print(f"使用HTTPS模式启动")
            app.run(host=host, port=port, use_https=True, cert_path=str(cert_path), key_path=str(key_path))
        else:
            print(f"使用HTTP模式启动")
            app.run(host=host, port=port)
    except Exception as e:
        print(f"启动应用时发生错误: {e}")
        print("请检查端口是否被占用，或者使用不同的端口启动应用。")
    finally:
        # 清理证书文件
        if use_https:
            print("清理证书文件...")
            app.cleanup_certificates(str(cert_path), str(key_path))

    input("按 Enter 键退出...")
