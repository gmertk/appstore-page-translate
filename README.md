# App Store Page Translation System

A simple translation script for App Store metadata translation supporting 34+ international markets.

## 🎯 Features

- ✅ **34 Language Support** - All official App Store locales
- ✅ **Smart Length Validation** - Automatic compliance with App Store character limits
- ✅ **Incremental Translation** - Only translates missing files to save costs
- ✅ **Quality Control** - Clean summary reporting of any issues
- ✅ **Fastlane Integration** - Ready for automated App Store uploads
- ✅ **GPT-4 Powered** - Translate with OpenAI API

## 🛠️ Setup

### Prerequisites

- Python 3.10+
- OpenAI API key
- Fastlane (optional, for App Store uploads)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/gmertk/appstore-page-translate.git
   cd appstore-page-translate
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Configure Fastlane for your app**
   Update `fastlane/Appfile` with your app details:
   ```ruby
   app_identifier("com.yourcompany.yourapp")
   apple_id("your-apple-id@example.com")
   ```

## 🚀 Usage

### 1. Edit Your English Content

Update the files in `fastlane/metadata/en-US/`:

- `name.txt` - App name (max 30 chars)
- `subtitle.txt` - App subtitle (max 30 chars)
- `description.txt` - App description
- `keywords.txt` - App Store keywords (max 100 chars)
- `promotional_text.txt` - Promotional text

### 2. Run Translation

```bash
python translate.py
```

The script will:

- 🌍 Process each language sequentially
- ⏭️ Skip existing translations
- 📝 Translate only missing files
- ✅ Validate character limits automatically
- 📊 Show a summary of any issues

### Sample Output

```
🌍 Processing German (de-DE)...
   ⏭️  Skipping name.txt - already exists
   ⏭️  Skipping subtitle.txt - already exists
   📝 Translating 1 files...
   ✅ Translated keywords.txt (89 chars)

✅ All translations written successfully!
✅ All metadata within App Store limits!
```

## 📏 Character Limits & Validation

The system automatically enforces App Store character limits:

| Field    | Limit          | Validation                         |
| -------- | -------------- | ---------------------------------- |
| App Name | 30 characters  | ✅ Auto-retry with shorter version |
| Subtitle | 30 characters  | ✅ Auto-retry with shorter version |
| Keywords | 100 characters | ✅ Smart truncation by priority    |

### Length Validation Process

1. **First attempt**: Normal high-quality translation
2. **If over limit**: Automatic retry with length constraints
3. **If still over**: Keep original, show in summary
4. **Keywords**: Smart truncation by removing less important terms

## 🚀 Fastlane Integration

### Configure Fastlane for Your App

Before uploading, update `fastlane/Appfile` with your app details:

```ruby
# fastlane/Appfile
app_identifier("com.yourcompany.yourapp") # Your app's bundle identifier
apple_id("your-apple-id@example.com")    # Your Apple ID email

# Optional: For App Store Connect API (recommended)
# app_store_connect_api_key(
#   key_id: "XXXXXXXXXX",
#   issuer_id: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
#   key_filepath: "./AuthKey_XXXXXXXXXX.p8"
# )
```

### Upload Metadata to App Store

```bash
cd fastlane
fastlane upload_metadata
```

## 🔧 Customization

### Adding New Languages

1. Add the locale code to `target_languages` in `translate.py`
2. Ensure the code matches official App Store locales
3. Run the translation script

### Modifying Translation Prompts

Edit the `system_prompt` variables in the `translate_text()` function to customize:

- Translation style
- Brand voice
- Specific instructions per file type

### Changing File Types

Modify the `files_to_translate` list to add/remove metadata files:

```python
files_to_translate = ["name.txt", "subtitle.txt", "description.txt", "keywords.txt", "promotional_text.txt"]
```

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Errors**

- Check your API key in `.env`
- Verify you have sufficient API credits
- Ensure stable internet connection

**Character Limit Warnings**

- Review files listed in the summary
- Manually edit overly long translations
- Re-run script to validate fixes

**Missing Translations**

- Delete specific language folders to re-translate
- Verify English source files exist

**Fastlane Upload Errors**

- Check your `fastlane/Appfile` configuration
- Verify your Apple ID has access to the app
- For two-factor authentication, consider using App Store Connect API keys
