# Gemini API Setup Instructions

## Getting Your Gemini API Key

1. **Visit Google AI Studio**
   - Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account

2. **Create an API Key**
   - Click "Create API Key"
   - Select a Google Cloud project or create a new one
   - Copy the generated API key

## Setting Up the API Key

### Option 1: Environment Variable (Recommended)

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="AIzaSyDwNP77GPVWYlrqfBpDCvYiegIqoQO3DRg"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Option 2: Permanent Setup

**Windows:**
1. Search for "Environment Variables" in Windows Search
2. Click "Edit the system environment variables"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `GEMINI_API_KEY`
6. Variable value: Your API key
7. Click OK

**Linux/Mac:**
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Running the Application

After setting up the API key:

```bash
python app.py
```

## Features Enabled by Gemini API

When the Gemini API key is configured, you'll get:

1. **✨ AI-Powered Destination Summary**
   - Engaging 2-3 sentence overview of the destination
   - Highlights what makes the place special

2. **💡 Travel Tips**
   - 3 practical, weather-aware travel tips
   - Personalized recommendations

3. **📍 Enhanced Attraction Information**
   - Detailed addresses for each tourist attraction
   - Better location context

## Without API Key

The application will still work without a Gemini API key, but:
- AI-powered summaries won't be displayed
- Travel tips won't be generated
- You'll still get weather and attraction information with addresses

## Troubleshooting

- **API Key Not Working**: Make sure you've set the environment variable in the same terminal where you run the app
- **Restart Required**: After setting environment variables permanently, restart your terminal or IDE
- **Rate Limits**: Free tier has usage limits. Check [Google AI Studio](https://makersuite.google.com/) for your quota

## API Costs

- Gemini 1.5 Flash has a generous free tier
- Check current pricing at [Google AI Pricing](https://ai.google.dev/pricing)
