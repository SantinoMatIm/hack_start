"""OpenAI API client with retry logic."""

import json
import time
from typing import Optional

from openai import OpenAI, APIError, RateLimitError, APIConnectionError

from src.config.settings import get_settings
from src.config.constants import AI_PARAMS


class OpenAIClient:
    """
    OpenAI API client with retry logic and error handling.

    Used to parametrize actions based on risk context.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        settings = get_settings()
        self.api_key = api_key or settings.openai_api_key
        self.model = model or AI_PARAMS["model"]
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            if not self.api_key:
                raise ValueError("OpenAI API key not configured")
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.3,
    ) -> Optional[str]:
        """
        Send completion request to OpenAI with retry logic.

        Args:
            system_prompt: System message setting context
            user_prompt: User message with specific request
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (lower = more deterministic)

        Returns:
            Response content or None if all retries fail
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

                return response.choices[0].message.content

            except RateLimitError as e:
                print(f"Rate limit hit, attempt {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1) * 2)  # Exponential backoff
                continue

            except APIConnectionError as e:
                print(f"Connection error, attempt {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                continue

            except APIError as e:
                print(f"API error, attempt {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                continue

            except Exception as e:
                print(f"Unexpected error: {e}")
                return None

        return None

    def complete_json(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.3,
    ) -> Optional[dict]:
        """
        Send completion request expecting JSON response.

        Args:
            system_prompt: System message
            user_prompt: User message
            max_tokens: Maximum tokens
            temperature: Sampling temperature

        Returns:
            Parsed JSON dict or None if failed
        """
        response = self.complete(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        if not response:
            return None

        # Try to extract JSON from response
        try:
            # Handle markdown code blocks
            content = response.strip()
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]

            return json.loads(content.strip())

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Response was: {response[:500]}")
            return None

    def is_available(self) -> bool:
        """Check if OpenAI API is available and configured."""
        try:
            if not self.api_key:
                return False
            # Quick test call
            self.client.models.list()
            return True
        except Exception:
            return False
