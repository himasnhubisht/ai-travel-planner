# Roamwise — AI Travel Planner Frontend

React + Vite frontend for the LangGraph/FastAPI travel planner.

## Run locally

1. Start your FastAPI backend in the existing project:
   ```powershell
   uvicorn main:app --reload
   ```
2. Open a second terminal in this frontend folder:
   ```powershell
   npm install
   npm run dev
   ```
3. Open the local URL Vite prints (usually http://localhost:5173).

The frontend calls `http://127.0.0.1:8000` by default. To change it, copy `.env.example` to `.env` and set `VITE_API_URL`.

## API expected

- `POST /trips` — accepts origin, destination, start_date, end_date, budget, travelers, interests.
- `POST /trips/{thread_id}/approval` — accepts `{ "approved": true|false, "feedback": "..." }`.

The approval response is expected to include the itinerary in either `itinerary` or `result.itinerary`. If your backend response format differs, update the small response-mapping section in `src/App.jsx`.

## Notes

- Never put API keys in frontend environment variables.
- The app uses live backend requests; there is no mock mode.
