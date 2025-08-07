import os
import sys
from translator import Translator
from language_selector import LanguageSelector
from file_selector import FileSelector
from metadata import AppMetadata


class TranslationManager:
    def __init__(self, api_key, languages, files_to_translate, en_dir):
        self.api_key = api_key
        self.language_selector = LanguageSelector(languages)
        self.file_selector = FileSelector(files_to_translate)
        self.app_metadata = AppMetadata(en_dir, files_to_translate)
        self.warnings = []

    def run(self):
        # Check if running in interactive mode
        is_interactive = sys.stdin.isatty()

        input_content = sys.stdin.read() if not is_interactive else ''
        input_lines = input_content.split('\n') if input_content else []

        lang_input = input_lines[0].strip() if input_lines and len(input_lines) > 0 else None
        file_input = input_lines[1].strip() if input_lines and len(input_lines) > 1 else None

        selected_languages = self.language_selector.select_languages(user_input=lang_input)
        selected_files = self.file_selector.select_files(user_input=file_input)

        if not self.api_key:
            print("❌ Error: OPENAI_API_KEY environment variable not set.")
            exit(1)
        self.translator = Translator(self.api_key)

        metadata_en, _ = self.app_metadata.load_english_metadata()

        for locale_code, language_name in selected_languages.items():
            output_dir = os.path.join("fastlane", "metadata", locale_code)
            os.makedirs(output_dir, exist_ok=True)

            print(f"🌍 Processing {language_name} ({locale_code})...")

            files_to_process = []
            for file_name in selected_files:
                target_file = os.path.join(output_dir, file_name)
                if os.path.exists(target_file):
                    print(f"   ⏭️  Skipping {file_name} - already exists")
                else:
                    files_to_process.append(file_name)

            if not files_to_process:
                print(f"   ✅ All files already exist for {language_name}")
                continue

            print(f"   📝 Translating {len(files_to_process)} files...")
            for file_name in files_to_process:
                source_text = metadata_en[file_name]
                translated_text = self.translator.translate_text(source_text, language_name, file_name)

                # Validate length constraints
                if file_name == "keywords.txt" and len(translated_text) > 100:
                    words = translated_text.split(',')
                    truncated = []
                    current_length = 0
                    for word in words:
                        word = word.strip()
                        if current_length + len(word) + 1 <= 100:  # +1 for comma
                            truncated.append(word)
                            current_length += len(word) + 1
                        else:
                            break
                    translated_text = ','.join(truncated)
                elif file_name in ["name.txt", "subtitle.txt"] and len(translated_text) > 30:
                    # Retry with more aggressive length constraint
                    retry_translation = self.translator.translate_text(
                        f"Translate this {file_name.replace('.txt', '')} to {language_name}, but MUST be under 30 characters: {source_text}",
                        language_name
                    )
                    if len(retry_translation) <= 30:
                        translated_text = retry_translation
                    else:
                        file_path = os.path.join(output_dir, file_name)
                        self.warnings.append(
                            f"{language_name} ({locale_code}): {file_path} EXCEEDS LIMIT - {len(translated_text)} chars (App Store limit: 30)")

                with open(os.path.join(output_dir, file_name), "w") as f:
                    f.write(translated_text)

                if file_name in ["keywords.txt", "name.txt", "subtitle.txt"]:
                    print(
                        f"   ✅ Translated {file_name} ({len(translated_text)} chars)")
                else:
                    print(f"   ✅ Translated {file_name}")

        print("✅ All translations written successfully!")
        self.display_summary()

    def display_summary(self):
        if self.warnings:
            print(f"\n⚠️  Files Exceeding App Store Limits ({len(self.warnings)} issues):")
            print("=" * 60)
            for warning in self.warnings:
                print(f"  • {warning}")
            print("=" * 60)
            print("Note: These files may cause upload failures in Fastlane.")
        else:
            print("\n✅ All metadata within App Store limits!")
