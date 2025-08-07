from openai import OpenAI


class Translator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def translate_text(self, text, target_language_name, file_name=None):
        if file_name == "keywords.txt":
            system_prompt = f"You are an expert App Store translator. Translate keywords into {target_language_name}. CRITICAL: The final result must be under 100 characters total. Use shorter synonyms, abbreviations, or remove less important terms if needed. Maintain comma separation and prioritize the most important keywords."
        elif file_name == "name.txt":
            system_prompt = f"You are an expert App Store translator. Translate the app name into {target_language_name}. CRITICAL: The result needs to be under 30 characters total. Keep the core meaning and brand identity."
        elif file_name == "subtitle.txt":
            system_prompt = f"You are an expert App Store translator. Translate the app subtitle into {target_language_name}. CRITICAL: The result must be under 30 characters total. Be concise and impactful while conveying the main value proposition."
        else:
            system_prompt = f"You are an expert App Store translator. Translate clearly and naturally into {target_language_name}. Keep format and tone professional and app-store appropriate."

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
