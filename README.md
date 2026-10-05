# NoteTaker - Personal Note Management Application

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates
- **LLM Translation**: Translate note title and content via OpenRouter (Nemotron free model)

## 🚀 Live Demo

The application is deployed on Vercel at: **https://mynotetaking.vercel.app**

(Screenshot with translation UI: [docs/screenshot-translation.png](docs/screenshot-translation.png))

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **SQLite** (local dev when `DATABASE_URL` is unset)
- **Neon Postgres** (production on Vercel via `DATABASE_URL`)

### AI
- **OpenRouter** with model `nvidia/nemotron-3-ultra-550b-a55b:free`

## 📁 Project Structure

```
MyNoteTaking/
├── database/
│   └── app.db               # SQLite database (created at runtime)
├── src/
│   ├── models/
│   │   ├── user.py          # User model (template)
│   │   └── note.py          # Note model with database schema
│   ├── routes/
│   │   ├── user.py          # User API routes (template)
│   │   └── note.py          # Note API endpoints
│   ├── static/
│   │   └── index.html       # Frontend application
│   └── main.py              # Flask application entry point
├── AGENTS.md                # Guide for AI coding agents
├── Makefile                 # install / dev / verify shortcuts
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🤖 AI assistants

See **[AGENTS.md](./AGENTS.md)** for architecture, API contracts, conventions, and verification commands used by Cursor and other agents.

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

   Remark: On Windows, use `venv\Scripts\activate`

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env: set OPENROUTER_API_KEY (required for translation)
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5001`

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes
- `POST /api/notes/translate` - Translate title and content (`target_language`, `title`, `content`)

### Request/Response Format
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "created_at": "2025-09-03T11:26:38.123456",
  "updated_at": "2025-09-03T11:27:30.654321"
}
```

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

### Notes Table
```sql
CREATE TABLE note (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Deployment (Vercel + Neon)

1. Create a [Neon](https://neon.tech) Postgres database and copy `DATABASE_URL`.
2. Import the GitHub repo in [Vercel](https://vercel.com) (Flask is auto-detected via `src/main.py`).
3. Set environment variables in the Vercel project:
   - `DATABASE_URL` — Neon connection string
   - `OPENROUTER_API_KEY` — OpenRouter API key
   - `OPENROUTER_MODEL` — `nvidia/nemotron-3-ultra-550b-a55b:free`
   - `SECRET_KEY` — random production secret
4. Deploy; `vercel.json` sets `maxDuration: 60` for translation requests.

## 🔧 Configuration

### Environment Variables
See `.env.example`. Key variables:
- `OPENROUTER_API_KEY` / `OPENROUTER_MODEL` — translation
- `DATABASE_URL` — Neon Postgres (omit locally for SQLite at `database/app.db`)
- `SECRET_KEY` — Flask secret
- `FLASK_ENV` — `development` for local debug

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the Flask server is running
3. Ensure all dependencies are installed
4. Check network connectivity for the deployed version

## 🎯 Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support
- Note categories and tags
- Rich text formatting (bold, italic, lists)
- File attachments
- Export functionality (PDF, Markdown)
- Dark/light theme toggle
- Offline support with service workers
- Note sharing capabilities

---

**Built with ❤️ using Flask, SQLite, and modern web technologies**

