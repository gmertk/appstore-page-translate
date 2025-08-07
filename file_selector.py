class FileSelector:
    def __init__(self, files):
        self.files = files

    def select_files(self, user_input=None):
        print("\nAvailable files for translation:")
        for i, file_name in enumerate(self.files):
            print(f"  {i + 1}: {file_name}")

        print("\nPress ENTER to translate all files, or enter the numbers of files to translate, separated by commas.")
        if user_input is None:
            try:
                user_input = input("Files to translate (e.g., 1, 3, 5): ")
            except EOFError:
                user_input = ""  # Treat EOF (running from a file) as empty input

        if not user_input.strip():
            print("\n✅ Translating all files.")
            return self.files

        try:
            selected_indices = [int(i.strip()) - 1 for i in user_input.split(',')]
            selected_files = [
                self.files[i]
                for i in selected_indices
                if 0 <= i < len(self.files)
            ]
            if not selected_files:
                print("⚠️ No files selected. Exiting.")
                exit()
            print("\n✅ Translating the following files:")
            for file_name in selected_files:
                print(f"  - {file_name}")
            return selected_files
        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by commas. Exiting.")
            exit()
