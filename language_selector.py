class LanguageSelector:
    def __init__(self, languages):
        self.languages = languages

    def select_languages(self, user_input=None):
        print("Available languages for translation:")
        language_list = list(self.languages.items())
        for i, (locale_code, language_name) in enumerate(language_list):
            print(f"  {i + 1}: {language_name} ({locale_code})")

        print("\nPress ENTER to translate all languages, or enter the numbers of languages to EXCLUDE, separated by commas.")
        if user_input is None:
            try:
                user_input = input("Languages to exclude (e.g., 1, 5, 12): ")
            except EOFError:
                user_input = ""  # Treat EOF (running from a file) as empty input

        if not user_input.strip():
            print("\n✅ Translating all languages.")
            return self.languages

        try:
            excluded_indices = [int(i.strip()) - 1 for i in user_input.split(',')]
            selected_languages = {
                locale_code: language_name
                for i, (locale_code, language_name) in enumerate(language_list)
                if i not in excluded_indices
            }
            if not selected_languages:
                print("⚠️ No languages selected. Exiting.")
                exit()
            print("\n✅ Translating the following languages:")
            for lang in selected_languages.values():
                print(f"  - {lang}")
            return selected_languages
        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by commas. Exiting.")
            exit()
