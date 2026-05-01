# Catfish King - Multi-Store Data Platform

Corporate dashboard for Great American Foods (Catfish King) to manage and analyze data across all restaurant locations.

## Features

- **Corporate Dashboard**: View aggregated data across all 11 locations
- **Store Dashboard**: Individual store management and data entry
- **Daily/Weekly Tracking**: Sales, food cost, labor cost, customers
- **Product Pricing**: Track vendor prices across locations
- **Role-Based Access**: Corporate admins and store managers

## Tech Stack

- Python Flask
- SQLite database
- Bootstrap UI

## Deployment

### Railway

1. Connect this repository to Railway
2. Set environment variables:
   - `SECRET_KEY`: Random secret string for sessions
3. Deploy

### Local Development

```bash
pip install -r requirements.txt
python app.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask session secret (required) |

## License

Proprietary - Great American Foods