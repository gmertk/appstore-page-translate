
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Target locales and their language names for better translation prompts
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

# Files to process
files_to_translate = ["name.txt", "subtitle.txt",
                      "description.txt", "keywords.txt", "promotional_text.txt", "release_notes.txt"]

# Read English metadata
en_dir = os.path.join("fastlane", "metadata", "en-US")
metadata_en = {}

# Build list of files that actually exist
available_files = []
for file_name in files_to_translate:
    file_path = os.path.join(en_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            metadata_en[file_name] = f.read().strip()
        available_files.append(file_name)

# Update files_to_translate to only include available files
files_to_translate = available_files


def translate_text(text, target_language_name, file_name=None):
    if file_name == "keywords.txt":
        system_prompt = f"You are an expert App Store translator. Translate keywords into {target_language_name}. CRITICAL: The final result must be under 100 characters total. Use shorter synonyms, abbreviations, or remove less important terms if needed. Maintain comma separation and prioritize the most important keywords."
    elif file_name == "name.txt":
        system_prompt = f"You are an expert App Store translator. Translate the app name into {target_language_name}. CRITICAL: The result needs to be under 30 characters total. Keep the core meaning and brand identity."
    elif file_name == "subtitle.txt":
        system_prompt = f"You are an expert App Store translator. Translate the app subtitle into {target_language_name}. CRITICAL: The result must be under 30 characters total. Be concise and impactful while conveying the main value proposition."
    else:
        system_prompt = f"You are an expert App Store translator. Translate clearly and naturally into {target_language_name}. Keep format and tone professional and app-store appropriate."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()


# Translate and write per locale
warnings = []
for locale_code, language_name in target_languages.items():
    output_dir = os.path.join("fastlane", "metadata", locale_code)
    os.makedirs(output_dir, exist_ok=True)

    print(f"🌍 Processing {language_name} ({locale_code})...")

    files_to_process = []
    for file_name in files_to_translate:
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
        translated_text = translate_text(source_text, language_name, file_name)

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
            # Keywords truncation is automatic and successful, no warning needed
        elif file_name in ["name.txt", "subtitle.txt"] and len(translated_text) > 30:
            original_length = len(translated_text)
            # Retry with more aggressive length constraint
            retry_prompt = f"Translate this {file_name.replace('.txt', '')} to {language_name}, but MUST be under 30 characters: {source_text}"
            retry_translation = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Translate to {language_name}. Result MUST be under 30 characters. Be extremely concise."},
                    {"role": "user", "content": retry_prompt}
                ]
            ).choices[0].message.content.strip()

            # If retry is successful, use it; otherwise keep original
            if len(retry_translation) <= 30:
                translated_text = retry_translation
                # Successful retranslation, no warning needed
            else:
                file_path = os.path.join(output_dir, file_name)
                warnings.append(
                    f"{language_name} ({locale_code}): {file_path} EXCEEDS LIMIT - {len(translated_text)} chars (App Store limit: 30)")
                # Keep the original translated_text as is

        with open(os.path.join(output_dir, file_name), "w") as f:
            f.write(translated_text)

        if file_name in ["keywords.txt", "name.txt", "subtitle.txt"]:
            print(
                f"   ✅ Translated {file_name} ({len(translated_text)} chars)")
        else:
            print(f"   ✅ Translated {file_name}")

print("✅ All translations written successfully!")

# Show warnings summary
if warnings:
    print(f"\n⚠️  Files Exceeding App Store Limits ({len(warnings)} issues):")
    print("=" * 60)
    for warning in warnings:
        print(f"  • {warning}")
    print("=" * 60)
    print("Note: These files may cause upload failures in Fastlane.")
else:
    print("\n✅ All metadata within App Store limits!")
