import os
from openai import OpenAI

class NemotronAgent:
    def __init__(self, api_key=None, model="nvidia/nemotron-4-340b-instruct"):
        self.api_key = api_key or os.environ.get("NEBIUS_API_KEY")
        self.model = model
        
        # Nebius Token Factory Endpoint
        self.client = OpenAI(
            base_url="https://api.studio.nebius.ai/v1/",
            api_key=self.api_key or "placeholder_key"
        )

    def generate_fix(self, buggy_code, description):
        prompt = f"""You are an expert Python developer. Fix the bug in the provided code.
Description: {description}

Buggy Code:
```python
{buggy_code}
