"""
Model Router — 统一AI模型调用客户端
支持 Mock 模式（无API Key时自动启用）和 真实API 模式
OpenAI 兼容协议，可一键切换 Base URL 和 API Key
"""

import time
import json
import random
import requests
from .mock_data import MockDataProvider

BASE_URL = "https://model-router.edu-aliyun.com/v1"


class ModelRouter:
    """统一的AI模型调用客户端，Mock模式与真实模式零代码切换"""

    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.mock_mode = not api_key
        self.mock = MockDataProvider()
        self._call_count = 0

    # ── 文本对话 ──────────────────────────────────────────

    def chat_completion(
        self,
        messages: list[dict],
        model: str = "qwen/qwen3.7-max",
        temperature: float = 0.8,
        stream: bool = False,
        **kwargs,
    ) -> dict:
        """
        OpenAI 兼容的 Chat Completions 调用。
        返回格式: {"choices": [{"message": {"content": "..."}}], ...}
        """
        if self.mock_mode:
            return self._mock_chat(messages, model)
        return self._real_chat(messages, model, temperature, stream, **kwargs)

    def chat_completion_stream(self, messages: list[dict], model: str = "qwen/qwen3.7-max", **kwargs):
        """流式文本生成，返回 generator"""
        if self.mock_mode:
            yield from self._mock_chat_stream(messages, model)
            return
        yield from self._real_chat_stream(messages, model, **kwargs)

    # ── 图片生成 ──────────────────────────────────────────

    def generate_image(
        self,
        prompt: str,
        model: str = "qwen/wan2.7-image-pro",
        n: int = 1,
        size: str = "1024x1024",
    ) -> dict:
        """
        OpenAI 兼容的图片生成调用。
        返回格式: {"data": [{"url": "..."}, ...]}
        """
        if self.mock_mode:
            return self._mock_image(prompt, n, size)
        return self._real_image(prompt, model, n, size)

    # ── 视觉理解 ──────────────────────────────────────────

    def vision_chat(
        self,
        image_urls: list[str],
        prompt: str,
        model: str = "qwen/qwen3-vl-plus",
    ) -> dict:
        """
        多模态视觉理解调用，分析图片内容。
        """
        if self.mock_mode:
            return self._mock_vision(image_urls, prompt, model)

        content = [{"type": "text", "text": prompt}]
        for url in image_urls:
            content.append({"type": "image_url", "image_url": {"url": url}})

        messages = [{"role": "user", "content": content}]
        return self._real_chat(messages, model, temperature=0.3)

    # ── 内部：Mock 实现 ───────────────────────────────────

    def _simulate_latency(self, lo: float = 0.3, hi: float = 1.5):
        """模拟真实 API 延迟"""
        time.sleep(random.uniform(lo, hi))

    def _mock_chat(self, messages: list[dict], model: str) -> dict:
        self._simulate_latency()
        self._call_count += 1
        prompt = messages[-1].get("content", "") if messages else ""
        system = messages[0].get("content", "") if messages and messages[0].get("role") == "system" else ""
        content = self.mock.get_chat_response(prompt, system)
        return self._make_response(content, model)

    def _mock_chat_stream(self, messages: list[dict], model: str):
        self._call_count += 1
        prompt = messages[-1].get("content", "") if messages else ""
        system = messages[0].get("content", "") if messages and messages[0].get("role") == "system" else ""
        content = self.mock.get_chat_response(prompt, system)
        # 逐词输出模拟流式
        words = content.split()
        for i, word in enumerate(words):
            chunk = {
                "choices": [{"delta": {"content": word + (" " if i < len(words) - 1 else "")}, "index": 0}],
                "id": f"mock-chunk-{self._call_count}-{i}",
            }
            yield chunk
            time.sleep(random.uniform(0.02, 0.08))

    def _mock_image(self, prompt: str, n: int, size: str) -> dict:
        self._simulate_latency(1.0, 2.5)
        self._call_count += 1
        urls = self.mock.get_image_urls(prompt, n, size)
        return {
            "created": int(time.time()),
            "data": [{"url": u} for u in urls],
        }

    def _mock_vision(self, image_urls: list[str], prompt: str, model: str) -> dict:
        self._simulate_latency(1.0, 2.0)
        self._call_count += 1
        content = self.mock.get_vision_response(image_urls, prompt)
        return self._make_response(content, model)

    # ── 内部：真实 API 实现 ───────────────────────────────

    def _real_chat(self, messages: list[dict], model: str, temperature: float, stream: bool, **kwargs) -> dict:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            **kwargs,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()

    def _real_chat_stream(self, messages: list[dict], model: str, **kwargs):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": model, "messages": messages, "stream": True, **kwargs}
        resp = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.startswith("data: ") and decoded != "data: [DONE]":
                    yield json.loads(decoded[6:])

    def _real_image(self, prompt: str, model: str, n: int, size: str) -> dict:
        url = f"{self.base_url}/images/generations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": model, "prompt": prompt, "n": n, "size": size}
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()

    # ── 工具方法 ──────────────────────────────────────────

    def _make_response(self, content: str, model: str) -> dict:
        return {
            "id": f"mock-{self._call_count}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }

    def extract_content(self, response: dict) -> str:
        """从 API 响应中提取文本内容"""
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return ""

    def extract_image_urls(self, response: dict) -> list[str]:
        """从图片生成 API 响应中提取URL列表"""
        try:
            return [item["url"] for item in response.get("data", [])]
        except (KeyError, TypeError):
            return []
