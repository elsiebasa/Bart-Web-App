# BART Real-Time Dashboard

A real-time BART transit dashboard that shows live departures and historical performance data.

## Features

- Real-time BART station departures
- Historical performance analytics
- Interactive station selection
- Color-coded train information
- Automatic updates every 30 seconds

## Setup and Running the Application

### Backend Setup

1. Create and activate the conda environment:
```bash
conda create -n bart-env python=3.9
conda activate bart-env
```

2. Install the required Python packages:
```bash
pip install flask==2.0.1 werkzeug==2.0.1 flask-cors requests
```

3. Start the Flask backend server:
```bash
python app.py
```

The backend will run on http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd bart-frontend
```

2. Install Node.js dependencies:
```bash
npm install --legacy-peer-deps
```

3. Start the React development server:
```bash
npm start
```

The frontend will run on http://localhost:3000

## Using the Dashboard

1. Open http://localhost:3000 in your web browser
2. Select a BART station from the dropdown menu
3. View real-time departures in the "Live Departures" tab
4. Check historical performance in the "Historical Data" tab
5. View station statistics in the "Historical Stats" tab

## Data Updates

- Live departure data updates automatically every 30 seconds
- Historical data is collected and processed through the ETL pipeline

## Troubleshooting

If you encounter any issues:

1. Make sure both servers are running (backend on port 5000, frontend on port 3000)
2. Check that you're using the correct versions of Flask (2.0.1) and Werkzeug (2.0.1)
3. If you see module errors, ensure all dependencies are installed correctly
4. For frontend issues, try clearing your browser cache or running `npm install --legacy-peer-deps`

## License

MIT 