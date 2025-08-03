import ssl
import requests
from langflow.custom import Component
from langflow.inputs import DropdownInput, StrInput, BoolInput
from langflow.io import Output
from langflow.schema.message import Message
import base64

# Temporary SSL workaround (remove in production)
ssl._create_default_https_context = ssl._create_unverified_context

class LangfusePromptComponent(Component):
    display_name = "Langfuse Prompt Manager"
    description = "Fetch and manage Langfuse prompts with version control"
    icon = "prompts"

    # Hardcoded public key (replace with your value)
    PUBLIC_KEY = "pk-***************-4626-a114-4a8dc***********"
    HOST = "http://langfuse-dev:3000"

    inputs = [
        DropdownInput(
            name="selected_prompt",
            display_name="Select Prompt",
            options=[],
            refresh_button=True,
            advanced=False
        ),
        StrInput(
            name="new_prompt_name",
            display_name="New Prompt Name",
            advanced=False
        ),
        StrInput(
            name="new_prompt_content",
            display_name="Prompt Content",
            advanced=False,
        ),
        DropdownInput(
            name="label",
            display_name="Label",
            options=["production", "staging", "latest"],
            value="production",
            advanced=False
        ),
        BoolInput(
            name="save_trigger",
            display_name="Save to Langfuse",
            advanced=False
        ),
        StrInput(
            name="secret_key",
            display_name="Secret Key",
            advanced=False
        )
    ]

    outputs = [
        Output(display_name="Prompt Content", name="content", method="get_prompt_content"),
        Output(display_name="Save Result", name="save_result", method="handle_save")
    ]

    def _get_auth_header(self):
        """Generate the Basic Auth header using PUBLIC_KEY and SECRET_KEY."""
        credentials = f"{self.PUBLIC_KEY}:{self.secret_key}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return f"Basic {encoded_credentials}"

    def update_build_config(self, build_config: dict, field_value: str, field_name: str | None = None):
        """Update the dropdown options for the selected prompt."""
        if field_name == "selected_prompt":
            build_config["selected_prompt"]["options"] = self._fetch_prompts_list()
        return build_config

    def _fetch_prompts_list(self):
        """Fetch the list of prompts from the Langfuse API."""
        try:
            response = requests.get(
                f"{self.HOST}/api/public/v2/prompts",
                headers={"Authorization": self._get_auth_header()}
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            prompts = response.json().get("data", [])
            return [p["name"] for p in prompts] or ["No prompts found"]
        except requests.exceptions.RequestException as e:
            print(f"Prompt fetch error: {e}")
            return ["Error loading prompts"]

    def _get_prompt_content(self, promptName: str):
        """Fetch the content of a specific prompt from the Langfuse API."""
        try:
            response = requests.get(
                f"{self.HOST}/api/public/v2/prompts/{promptName}",
                headers={"Authorization": self._get_auth_header()},
                params={"label": self.label, "type": "chat"}  # Specify the prompt type as 'chat'
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            prompt_data = response.json()
            print(f"Raw prompt data: {prompt_data}")  # Log the raw response for debugging

            # Check if the response contains the expected structure for a chat prompt
            if "prompt" in prompt_data and isinstance(prompt_data["prompt"], list):
                # Extract the chat messages
                chat_messages = prompt_data["prompt"]
                formatted_messages = []
                for message in chat_messages:
                    role = message.get("role", "unknown")
                    content = message.get("content", "")
                    formatted_messages.append(f"{role}: {content}")
                return "\n".join(formatted_messages)  # Return the chat messages as a single string
            else:
                print(f"Unexpected prompt data structure: {prompt_data}")
                return "Error: Unexpected prompt data structure"
        except requests.exceptions.RequestException as e:
            print(f"Content fetch error: {e}")
            return "Error loading content"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Error loading content"

    def _save_prompt(self, name: str, content: str):
        """Save a new prompt to the Langfuse API."""
        try:
            response = requests.post(
                f"{self.HOST}/api/public/v2/prompts",
                headers={"Authorization": self._get_auth_header()},
                json={
                    "name": name,
                    "prompt": [{"role": "system", "content": content}],  # Save as a chat prompt
                    "labels": [self.label],
                    "config": {"temperature": 0.7},
                    "type": "chat"  # Specify the prompt type as 'chat'
                }
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            return f"Prompt saved successfully! Version: {response.json().get('version')}"
        except requests.exceptions.RequestException as e:
            return f"Save failed: {str(e)}"

    async def get_prompt_content(self) -> Message:
        """Return the content of the selected prompt as a Message."""
        content = self._get_prompt_content(self.selected_prompt)
        return Message(text=content)

    async def handle_save(self) -> Message:
        """Handle saving a new prompt to Langfuse."""
        if self.save_trigger:
            result = self._save_prompt(
                self.new_prompt_name,
                self.new_prompt_content
            )
            return Message(text=result)
        return Message(text="Save not triggered")
