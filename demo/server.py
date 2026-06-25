"""
宠食记 PetDiet AI 后端服务
使用 DeepSeek API 实现宠物饮食咨询对话
"""
import os
import sys
import json
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'your-api-key-here')
DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

# 系统提示词 - 宠物饮食助手
SYSTEM_PROMPT = """你是 PetDiet AI，一个专业的宠物饮食健康助手。

## 你的能力：
1. **宠物饮食方案推荐**：根据宠物的品种、年龄、体重、健康状况定制饮食方案
2. **食物安全查询**：判断某种食物是否适合宠物食用
3. **鲜粮食谱生成**：提供详细的自制宠物食品食谱，包含食材清单和制作步骤
4. **生病期间饮食调整**：根据宠物的健康问题提供饮食建议

## 输出格式要求：
- 使用结构化输出，包含清晰的标题和分段
- 食谱类回复必须包含：食材清单表格、制作步骤、喂食建议
- 重要提醒使用表格对比展示
- 适当使用 emoji 增加可读性
- 语气友好专业，像一个懂宠物的朋友在提建议

## 重要限制：
- 你不做疾病诊断，遇到健康问题会建议咨询兽医
- 你会强调自制粮需要额外补充营养素
- 对于严重健康问题，你会建议及时就医

## 当前示例宠物信息：
- 名字：布丁
- 品种：金毛
- 年龄：3岁
- 体重：28.5kg
- 健康标签：鸡肉过敏、关节养护
"""

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        data = request.json
        messages = data.get('messages', [])

        if not messages:
            return jsonify({'error': '消息不能为空'}), 400

        # 构建API请求
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT}
            ] + messages,
            'temperature': 0.7,
            'max_tokens': 2000,
            'stream': False
        }

        # 调用 DeepSeek API
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return jsonify({'error': f'API调用失败: {response.text}'}), 500

        result = response.json()
        assistant_message = result['choices'][0]['message']['content']

        return jsonify({
            'success': True,
            'message': assistant_message,
            'usage': result.get('usage', {})
        })

    except requests.Timeout:
        return jsonify({'error': '请求超时，请重试'}), 504
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """处理流式聊天请求"""
    try:
        data = request.json
        messages = data.get('messages', [])

        if not messages:
            return jsonify({'error': '消息不能为空'}), 400

        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT}
            ] + messages,
            'temperature': 0.7,
            'max_tokens': 2000,
            'stream': True
        }

        def generate():
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                stream=True,
                timeout=30
            )

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]
                        if data.strip() == '[DONE]':
                            yield f'data: [DONE]\n\n'
                            break
                        try:
                            chunk = json.loads(data)
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    yield f'data: {json.dumps({"content": delta["content"]})}\n\n'
                        except json.JSONDecodeError:
                            continue

        return app.response_class(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )

    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

if __name__ == '__main__':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    print("宠食记 PetDiet AI 后端服务启动中...")
    print("访问地址: http://localhost:5000")
    print("请确保已设置 DEEPSEEK_API_KEY 环境变量")
    app.run(debug=True, port=5000)
