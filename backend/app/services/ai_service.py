import httpx
from typing import Optional
from app.core.config import settings


class AIService:
    """AI 服务 - 调用 阿里云 DashScope API 生成代码"""

    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL
        # 阿里云 DashScope API
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    async def generate_code(
        self,
        prompt: str,
        conversation_history: Optional[list] = None,
        current_code: Optional[dict] = None
    ) -> dict:
        """
        根据用户提示生成代码

        Args:
            prompt: 用户需求描述
            conversation_history: 对话历史列表
            current_code: 当前代码（包含 html, css, js）

        Returns:
            dict: 包含 html, css, js 的字典
        """
        system_prompt = """你是一个专业的前端代码生成助手。请根据用户需求生成完整的 HTML/CSS/JS 代码。
要求：
1. 代码要简洁、现代、可运行
2. HTML 结构清晰，语义化
3. CSS 样式美观，支持响应式
4. JS 功能完整，无错误

请严格按照以下 JSON 格式返回：
{
    "html": "<!DOCTYPE html>...",
    "css": "/* CSS 样式 */",
    "js": "// JavaScript 代码"
}

只返回 JSON 数据，不要有其他说明文字。"""

        # 构建对话消息
        messages = []

        # 添加系统提示
        messages.append({"role": "system", "content": system_prompt})

        # 如果有当前代码，添加到消息中
        if current_code and (current_code.get('html') or current_code.get('css') or current_code.get('js')):
            code_context = f"""当前应用的代码如下：
```html
{current_code.get('html', '')}
```
```css
{current_code.get('css', '')}
```
```javascript
{current_code.get('js', '')}
```

请根据用户的后续需求修改或完善代码。如果用户要求添加新功能，请在现有代码基础上进行扩展。"""
            messages.append({"role": "system", "content": code_context})

        # 添加对话历史
        if conversation_history:
            for msg in conversation_history[-10:]:  # 只保留最近 10 条消息
                # 处理 pydantic 模型或字典
                if hasattr(msg, 'role'):
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
                else:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })

        # 添加当前请求
        messages.append({"role": "user", "content": f"请帮我：{prompt}"})

        # 如果没有配置 API Key，返回示例代码
        if not self.api_key:
            return self._get_mock_code(prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": messages
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # 解析返回的 JSON
                import json
                import re

                # 如果内容被 markdown 代码块包裹，提取 JSON 部分
                json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)

                code_data = json.loads(content)
                return {
                    "html": code_data.get("html", ""),
                    "css": code_data.get("css", ""),
                    "js": code_data.get("js", "")
                }
        except httpx.TimeoutException as e:
            print(f"AI API 调用超时：{e}")
            return self._get_mock_code(prompt)
        except Exception as e:
            print(f"AI API 调用失败：{e}")
            # 降级返回示例代码
            return self._get_mock_code(prompt)

    def _get_mock_code(self, prompt: str) -> dict:
        """返回示例代码（用于演示）"""
        return {
            "html": """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生成的应用</title>
</head>
<body>
    <div class="container">
        <h1>欢迎使用 Atoms Demo</h1>
        <p>这是一个演示应用，展示了 AI 生成的网页结构。</p>
        <button id="actionBtn">点击我</button>
        <div id="output"></div>
    </div>
</body>
</html>""",
            "css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.container {
    background: white;
    padding: 2rem 3rem;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    text-align: center;
}

h1 {
    color: #333;
    margin-bottom: 1rem;
    font-size: 1.8rem;
}

p {
    color: #666;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 32px;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

#output {
    margin-top: 1.5rem;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
    min-height: 50px;
}""",
            "js": """document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('actionBtn');
    const output = document.getElementById('output');
    let clickCount = 0;

    btn.addEventListener('click', function() {
        clickCount++;
        output.innerHTML = '<p>按钮被点击了 <strong>' + clickCount + '</strong> 次！</p>';
        output.style.color = '#667eea';
    });

    console.log('应用已加载，等待用户交互...');
});"""
        }


ai_service = AIService()
