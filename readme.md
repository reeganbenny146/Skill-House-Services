# Skill House Services Application

## Overview

The Skill House Services Application is a multi-user web platform that connects service professionals with customers for a wide range of home services. The application has an admin panel for managing users and services, a customer interface for booking and reviewing services, and a professional interface for managing service requests.

## Features

### Admin Features:
- **User Management**: Admin can monitor, accept/reject, block/unblock, and delete professionals and customers.
- **Service Management**: Admin can add new services, categories, and manage service requests.
- **Graphical Insights**: Admin can view overall summary and insights using charts (Service vs Service Request, Service vs Professional, etc.).

### Customer Features:
- **Service Booking**: Customers can book new services, cancel requests (before acceptance), and close completed services.
- **Review System**: Customers can review professionals based on service quality.
- **Service Search**: Customers can search professionals by various criteria (location, pincode, services, etc.).
- **Summary View**: Customers can view charts and insights regarding their service requests.

### Professional Features:
- **Service Requests**: Professionals can accept, reject, or complete service requests.
- **Search & Filter**: Professionals can filter service requests by location and pincode.
- **Summary View**: Professionals can view charts related to service request status.

## Technologies Used
- **Flask**: Web framework for handling routes, templates, and logic.
- **Flask-SQLAlchemy**: ORM for database interaction.
- **Flask-Login**: For handling user authentication and session management.
- **Bootstrap**: For responsive and attractive UI.
- **ChartJS**: For rendering various graphs (Bar charts, Pie charts, etc.).
- **SQLite**: Database for storing user data, service requests, etc.

## API Endpoints

### User Registration (`/api/register`)
- **Method**: POST
- **Description**: Register a new user as a customer or professional.
- **Parameters**: 
    - `firstName`, `lastName`, `username`, `email`, `password`, `cpassword`, `role`, and additional professional-specific details (`experience`, `serviceType`, etc.).
  
### User Deletion (`/api/deleteUser`)
- **Method**: PUT or DELETE
- **Description**: Soft delete or permanently delete a user (customer/professional).
- **Parameters**: 
    - `userId`, `role` (specifying the user type).
  


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/reeganbenny146/Skill-House-Services.git
   cd household-services-app
   ```
2. Create and activate a venv:
    ```
    python -m venv project_env
    project_env\scripts\activate
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Run the application:
    ```
    flask run
    ```
    or
    ```
    python main.py
    ```



