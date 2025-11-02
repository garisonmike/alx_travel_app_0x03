# ALX Travel App 0x03

This project enhances the travel booking platform by integrating Celery with RabbitMQ
to handle email notifications asynchronously.

## Features
- Asynchronous email notifications for booking confirmations
- Non-blocking user experience using Celery
- RabbitMQ as a message broker for background tasks

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   sudo apt install rabbitmq-server
