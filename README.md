# HNG Stage 0 Backend Task - Name Classification API

## Project Overview
This is a backend API built using Django and Django REST Framework. It integrates the Genderize API to predict the gender associated with a given name and returns a structured, processed response based on defined rules.
The API enhances raw data from Genderize by adding:
- Confidence evaluation
- Standardized response format
- Timestamp metadata

---

## Tech Stack
* Python
* Django
* Django REST Framework (DRF)
* Requests
*  Django CORS Headers
* Vercel (Deployment)

---

## Setup Instructions (Local Development)

1. Clone the repository:

```bash
git clone https://github.com/Giftbatolu/hng-stage_0-api.git
cd hng-stage_0-api
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run server:
```bash
python manage.py runserver
```

5. Test endpoint:
```bash
http://127.0.0.1:8000/api/classify?name=anna
```

---

## API Endpoint

### Classify Name

**GET** `/api/classify?name={name}`

## Processing Logic

* Extracted fields from Genderize API:
    * `gender`
    * `probability`
    * `count` renamed to `sample_size`

* Confidence rule:
    * `is_confident = true` if: (probability ≥ 0.7 **AND** sample_size ≥ 100)

* Timestamp:
    * `processed_at` is generated dynamically in **UTC (ISO 8601 format)**

## Success Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
```

## Edge Case Handling
* If the API returns:  gender = null OR count = 0
```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

## Error Responses

### Missing Name (400)

```json
{
  "status": "error",
  "message": "Missing or empty name parameter"
}
```

### Invalid Name Type (422)

```json
{
  "status": "error",
  "message": "name must be a string"
}
```

### Server / Upstream Error (500 / 502)

```json
{
  "status": "error",
  "message": "Upstream API error"
}
```
## Deployment
This API is deployed on **Vercel** using a serverless configuration.

---

## Live API
🔗 https://hng-stage-0-api-opal.vercel.app/

---

## Example Request (cURL)
```bash
curl -X GET "https://hng-stage-0-api-opal.vercel.app/api/classify?name=anna"
```

---

## Author
**Sekinat Oyelami**

---

## Acknowledgment
This project was completed as part of the **HNG Internship Stage 0 Backend Task**.