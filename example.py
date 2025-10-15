
# New Vertex config
VERTEX_API_KEY = os.getenv('VERTEX_API_KEY') or app_config.get('vertex_api_key')

def _sanitize_model(raw: str) -> str:
    if not raw:
        return 'gemini-2.5-flash-lite'
    # Remove any inline comments after a # and strip whitespace
    cleaned = raw.split('#', 1)[0].strip()
    # Collapse internal whitespace just in case
    cleaned = ' '.join(cleaned.split())
    return cleaned or 'gemini-2.5-flash-lite'

VERTEX_MODEL = _sanitize_model(os.getenv('VERTEX_MODEL') or app_config.get('vertex_model') or 'gemini-2.5-flash-lite')

# Vertex endpoint base (publisher path model spec). We'll use streaming? For now non-streaming simple generate.
VERTEX_ENDPOINT = f"https://aiplatform.googleapis.com/v1/publishers/google/models/{VERTEX_MODEL}:generateContent"

# MSAL app removed for Vertex API key flow
msal_app = None

def allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

class LLMChatbot:
    """LLM Chatbot class now using Google Vertex AI Generative API via API key."""

    def __init__(self, api_key: str, model: str):
        if not api_key:
            raise ValueError("Vertex API key missing (VERTEX_API_KEY).")
        self.api_key = api_key
        self.model = model
        self.endpoint = f"https://aiplatform.googleapis.com/v1/publishers/google/models/{self.model}:generateContent"

    def _convert_messages(self, messages):
        """Convert legacy OpenAI-like message list into Vertex 'contents' structure.
        Input: [{'role': 'system'|'user'|'assistant', 'content': str}, ...]
        Vertex expects an array of contents objects by role with parts list.
        We'll map each message to a separate content entry preserving order.
        System messages will be prepended as a user instruction block.
        """
        contents = []
        for m in messages:
            role = m.get('role')
            text = m.get('content', '')
            if not text:
                continue
            # Vertex roles: 'user' and 'model'. We'll map system -> user, assistant -> model.
            if role == 'assistant':
                vertex_role = 'model'
            else:
                vertex_role = 'user'
            contents.append({
                'role': vertex_role,
                'parts': [{'text': text}]
            })
        return contents

    def send_chat_message(self, messages):
        """Send chat messages to Vertex AI and return concatenated model text response."""
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'contents': self._convert_messages(messages),
                # Basic generation config; can be parameterized later
                'generationConfig': {
                    'temperature': 0.7,
                    'topK': 40,
                    'topP': 0.95,
                    'maxOutputTokens': 512
                }
            }
            params = {'key': self.api_key}
            response = requests.post(self.endpoint, headers=headers, params=params, json=payload, timeout=30)
            if response.status_code != 200:
                raise Exception(f"Vertex API error {response.status_code}: {response.text}")
            data = response.json()
            # Non-streaming response: candidates[0].content.parts[].text
            candidates = data.get('candidates', [])
            if not candidates:
                raise Exception('No candidates returned from Vertex API')
            parts = candidates[0].get('content', {}).get('parts', [])
            text_fragments = [p.get('text', '') for p in parts if 'text' in p]
            return ''.join(text_fragments).strip() or '[No content returned]'
        except requests.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Chat request failed: {str(e)}")

# Initialize LLM Chatbot (Vertex)
llm_chatbot = LLMChatbot(VERTEX_API_KEY, VERTEX_MODEL) if VERTEX_API_KEY else None