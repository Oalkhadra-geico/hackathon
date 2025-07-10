# DOI Research Assistant - Integrated System

This system integrates the frontend UI with the backend LLM agent to provide a complete DOI (Department of Insurance) research assistant.

## 🏗️ System Architecture

```
Frontend (ReactPy UI) ←→ Backend (Flask API) ←→ LLM Agent ←→ OpenSearch
```

### Components:
- **Frontend**: ReactPy-based UI for data filtering and query input
- **Backend**: Flask API server that processes queries and filtered data
- **LLM Agent**: Processes queries using the existing agentic LLM backend
- **OpenSearch**: Vector database for document retrieval

## 🚀 Quick Start

### Prerequisites
1. OpenSearch running on `localhost:9200`
2. Python 3.8+ with required packages
3. ResponseData.xlsx indexed in OpenSearch

### Installation
```bash
# Install required packages
pip install -r requirements.txt

# Index the data (if not already done)
python text_retrieve.py
```

### Running the System
```bash
# Option 1: Use the integrated startup script
python start_integrated_system.py

# Option 2: Run components separately
# Terminal 1: Start backend
python backend_server.py

# Terminal 2: Start frontend
python ui/simple_react.py
```

## 📋 How to Use

### 1. Data Filtering
- Use the filter dropdowns to narrow down your dataset:
  - **State**: Filter by specific states
  - **Line of Business**: Filter by insurance types (AIP, Boat, Commercial, etc.)
  - **Filing Type**: Filter by filing categories (Form, Rate, Rule, etc.)
  - **Response Type**: Filter by response categories
  - **Topic**: Filter by specific topics (MTF, Rate Capping, Tariffs, etc.)
  - **Carrier**: Filter by insurance carriers

### 2. Query Input
- Enter your research question in the text area
- Examples:
  - "What are the most common objections for rate filings?"
  - "Analyze patterns in MTF objections across different states"
  - "What are the top issues with tariff filings?"

### 3. Submit Query
- Click the "🚀 Submit Query" button
- The system will:
  1. Send your query and filtered data to the backend
  2. Process the data through the LLM agent
  3. Return insights and analysis in the "Model Output" section

## 🔧 Backend API

### Endpoints

#### POST `/query`
Processes user queries with filtered data.

**Request Body:**
```json
{
  "query": "User's research question",
  "filtered_data": [...], // Array of filtered records
  "filter_summary": {
    "total_records": 150,
    "states": ["CA", "TX"],
    "lobs": ["Personal Auto"],
    "filing_types": ["Rate"],
    "response_types": ["DOI Objection"],
    "topics": ["MTF", "Rate Capping"],
    "carriers": ["GEICO"]
  }
}
```

**Response:**
```json
{
  "response": "LLM analysis and insights",
  "query": "Original query",
  "filter_summary": {...},
  "records_analyzed": 150
}
```

#### GET `/health`
Health check endpoint.

## 🎯 Features

### Frontend Features
- ✅ Interactive data filtering
- ✅ Real-time filter updates
- ✅ Query input with validation
- ✅ Loading states and error handling
- ✅ Responsive design
- ✅ Beautiful UI with GEICO branding

### Backend Features
- ✅ Flask API server with CORS support
- ✅ Integration with existing LLM agent
- ✅ Comprehensive error handling
- ✅ Data processing and context creation
- ✅ Health check endpoint

### Integration Features
- ✅ Seamless frontend-backend communication
- ✅ Filtered data context for LLM
- ✅ Real-time query processing
- ✅ Comprehensive analysis output

## 🐛 Troubleshooting

### Common Issues

1. **"Cannot connect to backend"**
   - Ensure backend server is running on port 5000
   - Check if Flask server started successfully

2. **"No data available with current filters"**
   - Adjust your filter selections
   - Ensure ResponseData.xlsx is properly loaded

3. **"Error processing query"**
   - Check if OpenSearch is running on localhost:9200
   - Verify that data is indexed in OpenSearch
   - Check LLM API connectivity

4. **Excel file loading issues**
   - Ensure openpyxl is installed: `pip install openpyxl`
   - Verify ResponseData.xlsx exists in the correct location

### Debug Mode
```bash
# Run with debug output
FLASK_DEBUG=1 python backend_server.py
```

## 📊 Data Flow

1. **User Interaction**: User selects filters and enters query
2. **Data Filtering**: Frontend filters the dataset based on selections
3. **Query Submission**: Frontend sends query + filtered data to backend
4. **Backend Processing**: 
   - Creates context from filtered data
   - Builds comprehensive prompt
   - Calls LLM agent
5. **Response**: LLM analysis is returned to frontend
6. **Display**: Results shown in "Model Output" section

## 🔄 Development

### Adding New Features
1. **Frontend**: Modify `ui/simple_react.py`
2. **Backend**: Modify `backend_server.py`
3. **LLM Logic**: Modify `agent.py` or `completion.py`

### Testing
```bash
# Test backend API
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "filtered_data": [], "filter_summary": {}}'

# Test health endpoint
curl http://localhost:5000/health
```

## 📝 Notes

- The system preserves all existing backend logic
- No changes to the core LLM agent functionality
- Frontend provides an intuitive interface for data exploration
- Backend handles the complexity of data processing and LLM integration
- Error handling ensures graceful degradation