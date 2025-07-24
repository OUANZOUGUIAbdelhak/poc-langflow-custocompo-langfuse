# 📦 Langfuse Prompt Manager Component

This repository contains a custom [Langflow](https://github.com/logspace-ai/langflow) component that integrates with the [Langfuse](https://www.langfuse.com/) API to manage prompts with version control.

It allows you to fetch, preview, and save `chat`-style prompts to Langfuse directly from the Langflow UI.

---

## 🚀 Features

- 🔄 Fetch available prompts from Langfuse
- 🧠 Display content of a selected prompt (supports `chat` format)
- 💾 Save new prompts with name, content, and label
- ✅ Support for versioning and environment labels (`production`, `staging`, `latest`)
- 🔐 Basic authentication using public and secret keys
- 🛠️ Dynamic dropdown updates and interactive inputs via Langflow

---

## ⚙️ Inputs & Outputs

### 🔽 Inputs

| Name               | Type       | Description                                  |
|--------------------|------------|----------------------------------------------|
| `selected_prompt`  | Dropdown   | Select an existing prompt                    |
| `new_prompt_name`  | Text       | Name for the new prompt                      |
| `new_prompt_content` | Text     | Prompt content in chat format                |
| `label`            | Dropdown   | Prompt label (`production`, `staging`, etc.) |
| `save_trigger`     | Boolean    | Trigger the save operation                   |
| `secret_key`       | Text       | Langfuse secret key                          |

### 📤 Outputs

| Name         | Description                                 |
|--------------|---------------------------------------------|
| `content`    | Fetched content of the selected prompt      |
| `save_result`| Result message after saving the prompt      |

---

## 🛡️ Security Warning

> ⚠️ This implementation includes a **temporary SSL bypass** for development purposes:
>
> ```python
> ssl._create_default_https_context = ssl._create_unverified_context
> ```
>
> Make sure to **remove this line in production** to avoid insecure connections.

---

## 🛠️ Setup

To use this component inside Langflow:

1. Clone this repository.
2. Add the component class to your Langflow project.
3. Replace the `PUBLIC_KEY` and `HOST` variables with your Langfuse setup.
4. Use Langflow’s UI to connect inputs and outputs.

---

## 📜 License

This project is for educational or internal use. Please adapt to your production needs.

---

## 🙋‍♂️ Questions?

Feel free to open an issue if you need help or want to suggest improvements.
