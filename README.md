## Novastrum Market API

A scalable REST API for an intergalactic marketplace featuring role-based user systems, real-time bidding, and complex transaction management.

## Overview

Novastrum Market is a FastAPI-based backend service that simulates an intergalactic black market economy. The system supports multiple user roles (civilians, miners, chemists, government officials) with tier-based progression, marketplace transactions, substance trading, and war bidding mechanics.

## Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Server**: Uvicorn ASGI
- **Authentication**: Custom API key middleware
- **Database Tools**: Supabase (optional), psycopg2-binary

## Key Features

- **Role-Based Access Control**: 4-tier user progression system with dedicated modules (`citizen.py`, `miner.py`, `chemist.py`, `govt.py`)
- **Marketplace System**: Buy/sell substances and narcotics via `market.py`
- **Real-Time Bidding**: War betting with dynamic pricing through `bids.py`
- **Transaction Management**: Complete purchase workflows in `transaction.py`
- **Inventory System**: User-specific item management via `inventory.py`
- **Database Relationships**: 9 normalized tables with foreign key constraints

## Database Schema

The system uses a normalized PostgreSQL database with the following core entities:
- `citizens` - User accounts with role-based permissions
- `inventory` - User-owned items and currency (Voidex)
- `market` - Active marketplace listings
- `transactions` - Purchase history and cart management
- `wars` - Biddable conflicts between planets
- `bids` - User war betting records
- `substances` & `narcos` - Tradeable items with rarity systems


### Example Endpoints

- `POST /citizen/create` - User registration
- `POST /citizen/login` - Authentication
- `GET /inventory/audit` - View user inventory
- `GET /market/` - Browse marketplace
- `POST /transaction/` - Start purchase
- `GET /bids/wars` - View active wars
- `POST /bids/place` - Place war bets

## Architecture

The application follows a modular architecture with separate routers for each domain:

```
src/
├── api/
│   ├── citizen.py      # User management
│   ├── inventory.py    # Item management
│   ├── market.py       # Marketplace operations
│   ├── transaction.py  # Purchase workflows
│   ├── bids.py         # War betting system
│   ├── miner.py        # Mining operations
│   ├── chemist.py      # Narcotic brewing
│   ├── govt.py         # Government operations
│   ├── narco.py        # Narcotic management
│   ├── auth.py         # Authentication middleware
│   ├── populate.py     # Database seeding
│   └── server.py       # FastAPI app configuration
├── database.py         # Database connection
└── __init__.py
```

## Contributors

- **Sri Bala** - srbala@calpoly.edu
- **Bryce Kennedy** - bkenne06@calpoly.edu  
- **Ethan Swenke** - eswenke@calpoly.edu
- **Sofia Bryukhova** - sbryukho@calpoly.edu

## 📄 License

This project was developed as part of a database systems course at Cal Poly San Luis Obispo.
