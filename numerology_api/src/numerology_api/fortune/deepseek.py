import json
import logging
import time
from typing import Any

import httpx

from numerology_api.fortune.config import fortune_config

log = logging.getLogger("numerology_api.deepseek")


class DeepSeekError(Exception):
    pass


async def chat_json(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    if not fortune_config.api_key:
        log.error("DEEPSEEK_API_KEY 未配置")
        raise DeepSeekError("DEEPSEEK_API_KEY 未配置")

    payload = {
        "model": fortune_config.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.7,
    }
    headers = {
        "Authorization": f"Bearer {fortune_config.api_key}",
        "Content-Type": "application/json",
    }
    url = f"{fortune_config.base_url}/chat/completions"
    log.info(
        f"→ DeepSeek POST model={fortune_config.model} "
        f"prompt_chars=(sys:{len(system_prompt)}, user:{len(user_prompt)})"
    )
    t0 = time.perf_counter()

    try:
        async with httpx.AsyncClient(timeout=fortune_config.timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
    except httpx.HTTPError as e:
        dt = (time.perf_counter() - t0) * 1000
        log.error(f"✗ DeepSeek 网络异常 in {dt:.1f}ms: {e}")
        raise DeepSeekError(f"调用 DeepSeek 失败: {e}") from e

    dt = (time.perf_counter() - t0) * 1000
    if resp.status_code != 200:
        log.error(f"✗ DeepSeek 非 200 ({resp.status_code}) in {dt:.1f}ms: {resp.text[:300]}")
        raise DeepSeekError(f"DeepSeek 返回 {resp.status_code}: {resp.text[:200]}")

    data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        log.error(f"✗ DeepSeek 响应结构异常: {data}")
        raise DeepSeekError(f"响应结构异常: {data}") from e

    usage = data.get("usage") or {}
    log.info(
        f"← DeepSeek OK in {dt:.1f}ms "
        f"tokens=(prompt:{usage.get('prompt_tokens','?')}, "
        f"completion:{usage.get('completion_tokens','?')}) "
        f"content_chars={len(content)}"
    )

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        log.error(f"✗ DeepSeek 返回非 JSON: {content[:300]}")
        raise DeepSeekError(f"返回内容非 JSON: {content[:200]}") from e
