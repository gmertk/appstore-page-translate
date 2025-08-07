import os


class AppMetadata:
    def __init__(self, en_dir, files_to_translate):
        self.en_dir = en_dir
        self.files_to_translate = files_to_translate
        self.metadata_en = {}
        self.available_files = []

    def load_english_metadata(self):
        for file_name in self.files_to_translate:
            file_path = os.path.join(self.en_dir, file_name)
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    self.metadata_en[file_name] = f.read().strip()
                self.available_files.append(file_name)
        # Update files_to_translate to only include available files
        self.files_to_translate = self.available_files
        return self.metadata_en, self.files_to_translate
