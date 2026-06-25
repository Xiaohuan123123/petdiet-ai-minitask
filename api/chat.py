"""Vercel Serverless Function - Chat API"""
import os
import json
import requests
from http.server import BaseHTTPRequestHandler

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

SYSTEM_PROMPT = """你是宠食记 PetDiet AI，一个专业的宠物饮食健康助手。

你的能力：
1. 宠物饮食方案推荐：根据品种、年龄、体重、健康状况定制
2. 食物安全查询：判断食物是否适合宠物食用
3. 鲜粮食谱生成：提供详细的自制宠物食品食谱
4. 生病期间饮食调整建议

输出要求：结构化输出，食谱类需包含食材清单表格+制作步骤+注意事项。语气友好专业。

重要：不做疾病诊断，健康问题建议咨询兽医。"""

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            messages = data.get("messages", [])

            if not messages:
                self._send_error(400, "消息不能为空")
                return

            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": False
            }

            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)

            if response.status_code != 200:
                self._send_error(500, f"API调用失败: {response.text[:200]}")
                return

            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]

            self._send_json({
                "success": True,
                "message": assistant_message,
                "usage": result.get("usage", {})
            })

        except requests.Timeout:
            self._send_error(504, "请求超时，请重试")
        except Exception as e:
            self._send_error(500, f"服务器错误: {str(e)}")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _send_json(self, data):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _send_error(self, code, message):
        self.send_response(code)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}, ensure_ascii=False).encode("utf-8"))

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
