# Starting the Web Server

## Quick Start

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask web server**:
   ```bash
   python app.py
   ```

3. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

4. **Enter a place name** in the search box and click "Search"

## Features

- **Modern UI**: Beautiful gradient design with smooth animations
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Real-time Search**: Instant results with loading indicators
- **Error Handling**: Clear error messages for invalid places
- **Interactive**: Hover effects and smooth transitions

## API Endpoint

The web app uses a REST API endpoint:

- **URL**: `/api/search`
- **Method**: POST
- **Body**: `{ "place": "Paris" }`
- **Response**: JSON with tourism information

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.


