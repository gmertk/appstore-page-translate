
import os
from dotenv import load_dotenv
from translation_manager import TranslationManager

load_dotenv()


def main():
    # Configuration
    target_languages = {
        "ar-SA": "Arabic (Saudi Arabia)",
        "ca": "Catalan",
        "cs": "Czech",
        "da": "Danish",
        "de-DE": "German",
        "el": "Greek",
        "es-ES": "Spanish (Spain)",
        "es-MX": "Spanish (Mexico)",
        "fi": "Finnish",
        "fr-CA": "French (Canada)",
        "fr-FR": "French (France)",
        "he": "Hebrew",
        "hi": "Hindi",
        "hr": "Croatian",
        "hu": "Hungarian",
        "id": "Indonesian",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "ms": "Malay",
        "nl-NL": "Dutch",
        "no": "Norwegian",
        "pl": "Polish",
        "pt-BR": "Portuguese (Brazil)",
        "pt-PT": "Portuguese (Portugal)",
        "ro": "Romanian",
        "ru": "Russian",
        "sk": "Slovak",
        "sv": "Swedish",
        "th": "Thai",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "vi": "Vietnamese",
        "zh-Hans": "Chinese (Simplified)",
        "zh-Hant": "Chinese (Traditional)"
    }
    files_to_translate = ["name.txt", "subtitle.txt",
                          "description.txt", "keywords.txt", "promotional_text.txt", "release_notes.txt"]
    en_dir = os.path.join("fastlane", "metadata", "en-US")
    api_key = os.environ.get("OPENAI_API_KEY")

    # Run translation process
    manager = TranslationManager(
        api_key=api_key,
        languages=target_languages,
        files_to_translate=files_to_translate,
        en_dir=en_dir
    )
    manager.run()


if __name__ == "__main__":
    main()
