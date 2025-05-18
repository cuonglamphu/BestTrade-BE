# TradingView Backend

This is the backend service for the TradingView application, built with Flask and SocketIO to provide real-time trading data and functionality.

## Technologies Used

-   Python
-   Flask
-   Flask-SocketIO
-   Other dependencies (listed in requirements.txt)

## Prerequisites

Before you begin, ensure you have the following installed:

-   Python 3.x
-   pip (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone [your-repository-url]
cd backend
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following variables:

```env
HOST=localhost
PORT=5000
DEBUG=True
```

## Running the Application

To start the development server:

```bash
python run.py
```

The server will start at `http://localhost:8000` by default.

## Project Structure

```
backend/
├── app/
│   ├── config/
│   │   └── settings.py
│   ├── __init__.py
│   └── [other app modules]
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## API Documentation

You can find the API documentation at `http://localhost:8000/docs`

## Development

-   The application uses Flask for REST API endpoints
-   Real-time updates are handled through SocketIO
-   Configuration settings can be found in `app/config/settings.py`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
