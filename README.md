# Fitness Analytics Platform

A full-stack fitness analytics web application that tracks running, nutrition, and body weight to generate performance insights and trends.

## Features (Planned)
- Run logging and performance tracking
- Nutrition and macro tracking
- Body weight tracking
- Analytics dashboard
- Derived training metrics
- Background analytics processing

## Tech Stack

Frontend
- Next.js
- React
- TailwindCSS

Backend
- FastAPI
- Python
- SQLAlchemy

Infrastructure
- PostgreSQL
- Redis
- Docker

## Architecture

Frontend (Next.js)
↓
Backend API (FastAPI)
↓
PostgreSQL (data storage)
↓
Redis Queue (background jobs)
↓
Worker processes analytics

## Project Status

🚧 Currently in development

Initial setup complete:
- Project structure
- FastAPI backend
- Next.js frontend
- GitHub repository

Next milestone:
- PostgreSQL integration