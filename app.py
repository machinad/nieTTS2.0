from quart import Quart,render_template,request,jsonify
import os
import win32com.client
import edge_tts
import uuid
import pygame
import json
import httpx
import subprocess
from pythonosc import udp_client
from pathlib import Path
import dashscope 
from dashscope.audio.tts_v2 import SpeechSynthesizer as SpeechSynthesizerV2
from dashscope.audio.tts import SpeechSynthesizer as SpeechSynthesizerV1
class TTSWebApp:
    def __init__(self):
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
        self.local_tts_process = None
        self.GPTvts_voices_path = Path("./GPTvts_voices").resolve()
        self.GPTvts_path = Path("./GPTvts").resolve()
        self.GPTvts_path.parent.mkdir(parents=True, exist_ok=True)#
        self.GPTvts_voices_path.parent.mkdir(parents=True, exist_ok=True)
        self.local_interpreter_path = os.path.join(self.GPTvts_path, "GPT-SoVITS-v4-20250422fix",'runtime', 'python.exe')
        self.local_script_path = os.path.join(self.GPTvts_path, "GPT-SoVITS-v4-20250422fix",'api_v2.py')
        self.local_script_cwd = os.path.join(self.GPTvts_path, "GPT-SoVITS-v4-20250422fix")
        try:
            self.local_tts_process = subprocess.Popen(
                [
                    self.local_interpreter_path,
                    self.local_script_path,
                    '-a', '127.0.0.1',
                    '-p', '9880',
                    '-c', 'GPT_SoVITS/configs/tts_infer.yaml'
                ],
                cwd=self.local_script_cwd,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0,
            )
            if self.local_tts_process.poll() is not None:
                print(f"启动失败，进程返回码：{self.local_tts_process.poll()}")
                stderr_output = self.local_tts_process.stderr.read()
                if stderr_output:
                    print(f"错误输出：{stderr_output}")
                self.local_tts_process = None
            else:
                print("本地 TTS 服务脚本已启动。")
        except Exception as e:
            print(f"启动本地TTS服务失败: {e}")
            self.local_tts_process = None
        self.config_file = Path("./config.json")
        self.user_config = self.load_config()
        self.app = Quart(__name__)
        self.current_device = "default"
        self.tts_providers = [
            "Edge TTS",
            "阿里百炼cosyvice",
            "阿里百炼sambert",
            "GPTvts本地推理"
        ]
        self.savePath = Path("./save")
        self.setup_routes()
        self.osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
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
            "GPTvts_speed_factor":1
        }
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as file:
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
        设置路由
        """
        self.app.route('/')(self.index)
        self.app.route('/tts', methods=['POST'])(self.tts_endpoint)
        self.app.route("/get_voice_list")(self.get_voice_list)
    async def index(self):
        """
        /,主页
        """
        providers = self.tts_providers
        audio_devices = self.get_audio_devices()
        return await render_template('index.html',
                                    providers=providers,
                                    edge_tts_voices=self.Edge_TTS_voices,
                                    audio_devices=audio_devices,
                                    ali_tts_voices=list(self.ali_tts_voices.keys()),
                                    sambert_tts_voices=list(self.sambert_tts_voices.keys()),
                                    user_config = self.user_config
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
            "GPTvts_speed_factor":data.get("GPTvts_speed_factor", 1.0)
        }
        self.save_config(config_to_save)
        self.user_config = config_to_save
        text = data.get('text', '')
        device = data.get('device', '')
        self.set_audio_device(device)
        id = uuid.uuid4().hex
        temp_file = self.savePath / f"save_voice_{id}.mp3"
        if data.get("provider") == "GPTvts本地推理":
            temp_file = self.savePath / f"save_voice_{id}.wav"
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
            if await self.play_audio(temp_file):
                print(f"已播放音频文件: {temp_file}")
            else:
                print("播放音频文件失败")
                return jsonify({'error': "音频播放失败"}), 400
            if hasattr(pygame.mixer, 'get_init') and pygame.mixer.get_init():
                pygame.mixer.quit()
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print(f"已清理临时文件: {temp_file}")
                return jsonify({'status': 'success', 'message': '转换并播放完成'})
        if data.get("provider") == "阿里百炼cosyvice":
            if await self.use_ali_tts(data,temp_file):
                print(f"已转使用阿里百炼换文本: 生成临时文件{temp_file}")
            else:
                print("阿里百炼转换失败")
                return jsonify({'error': "tts转换失败"}), 400
            if await self.play_audio(temp_file):
                print(f"已播放音频文件: {temp_file}")
            else:
                print("播放音频文件失败")
                return jsonify({'error': "音频播放失败"}), 400
            if hasattr(pygame.mixer, 'get_init') and pygame.mixer.get_init():
                pygame.mixer.quit()
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print(f"已清理临时文件: {temp_file}")
                return jsonify({'status':'success','message': '转换并播放完成'})
        if data.get("provider") == "阿里百炼sambert":
            if await self.use_sambert_tts(data,temp_file):
                print(f"已转使用阿里百炼sambert模型换文本: 生成临时文件{temp_file}")
            else:
                print("阿里百炼sambert模型转换失败")
                return jsonify({'error': "tts转换失败"}), 400
            if await self.play_audio(temp_file):
                print(f"已播放音频文件: {temp_file}")
            else:
                print("播放音频文件失败")
                return jsonify({'error': "音频播放失败"}), 400
            if hasattr(pygame.mixer, 'get_init') and pygame.mixer.get_init():
                pygame.mixer.quit()
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print(f"已清理临时文件: {temp_file}")
                return jsonify({'status':'success','message': '转换并播放完成'})
        if data.get("provider") == "GPTvts本地推理":
            if await self.use_GPTvts(data,temp_file):
                print(f"已转使用GPTvts换文本: 生成临时文件{temp_file}")
            else:
                print("GPTvts模型转换失败")
                return jsonify({'error': "tts转换失败"}), 400
            if await self.play_audio(temp_file):
                print(f"已播放音频文件: {temp_file}")
            else:
                print("播放音频文件失败")
                return jsonify({'error': "音频播放失败"}), 400
            if hasattr(pygame.mixer, 'get_init') and pygame.mixer.get_init():
                pygame.mixer.quit()
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print(f"已清理临时文件: {temp_file}")
                return jsonify({'status':'success','message': '转换并播放完成'})
    async def get_voice_list(self):
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
                pygame.time.Clock().tick(10)
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
        url = "http://127.0.0.1:9880/tts"
        ref_audio_path = os.path.join(self.GPTvts_voices_path, data.get("GPTvts_character"),data.get("GPTvts_emotion"),data.get("GPTvts_sample"))
        ref_audio = data.get("GPTvts_sample")
        start_index = ref_audio.find("】")+1
        end_index = ref_audio.find(".wav")
        extracted_text = ref_audio[start_index:end_index]
        print("使用GPTvts模型服务转换文本，当前模型为"+ref_audio_path)
        json = {
            "text": data.get("text",""),
            "text_lang": "zh",
            "ref_audio_path": ref_audio_path,
            "aux_ref_audio_paths": [],
            "prompt_text": extracted_text,
            "prompt_lang": "zh",
            "top_k": 5,
            "top_p": 1,
            "temperature": 1,
            "text_split_method": "cut0",
            "batch_size": 1,
            "batch_threshold": 0.75,
            "split_bucket": True,
            "speed_factor":data.get("GPTvts_speed_factor",1),
            "streaming_mode": False,
            "seed": -1,
            "parallel_infer": True,
            "repetition_penalty": 1.35,
            "sample_steps": 32,
            "super_sampling": False
            }
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=json, headers=headers,timeout=120)
            except Exception as e:
                print(f"请求GPTvts服务失败: {e}")
                return False
            if response.status_code == 200:
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
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
    def set_audio_device(self, device):
        """
        设置音频输出设备
        """
        self.current_device = device
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
        if self.local_tts_process and self.local_tts_process.poll() is None:
            print("正在终止本地 TTS 服务脚本...")
            self.local_tts_process.terminate()
            try:
                self.local_tts_process.wait(timeout=5) # 等待子进程终止
                print("本地 TTS 服务脚本已终止。")
            except subprocess.TimeoutExpired:
                print("本地 TTS 服务脚本未在规定时间内终止，强制杀死。")
                self.local_tts_process.kill()
    def run(self,host,port):
        try:
            self.app.run(host=host,port=port)
        finally:
            self.cleanup()
if __name__ == '__main__': 
    app = TTSWebApp()
    app.run(host='0.0.0.0', port=1145)
