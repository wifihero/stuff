import requests

class LLMTranslator:
    def __init__(self, api_url="http://localhost:1234/v1"):
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json"
        }

    def translate_text_lines(self, text_lines, target_language, max_lines_per_chunk=100):
        """
        Sends chunked text lines to the LLM for translation. Each chunk contains a maximum of `max_lines_per_chunk` lines.
        """
        translated_lines = []

        for i in range(0, len(text_lines), max_lines_per_chunk):
            # Prepare a chunk of text lines
            chunk = text_lines[i:i + max_lines_per_chunk]
            numbered_text = "\n\n".join(chunk)

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a subtitle translation assistant. Translate the following text into the specified language, preserving the line numbering format exactly as provided. Do not skip any lines."
                    },
                    {
                        "role": "user",
                        "content": f"Translate the following text into {target_language}:\n\n{numbered_text}"
                    }
                ]
            }

            try:
                response = requests.post(self.api_url + "/chat/completions", headers=self.headers, json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors
                result = response.json()

                # Extracting the response content
                translated_text = result['choices'][0]['message']['content'].strip()
                translated_lines.extend(translated_text.split("\n\n"))

            except requests.exceptions.RequestException as e:
                print(f"Error during translation request: {str(e)}")
                return None

        return translated_lines