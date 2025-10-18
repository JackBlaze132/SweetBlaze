# SweetBlaze
real-time notification client for a candy shop called SweetBlaze, using Django (or Python) for the backend with WebSockets, and Vue + Ionic for the frontend. Notifications must support file uploads (e.g., images or PDFs) and display them dynamically in the UI. The project focuses on functionality, clean code, and simple but effective UX/UI design.

## Objective

Build a simple web application for a candy store called “SweetBlaze” that displays real-time notifications sent from a backend built with Django (or Python) to a frontend made with Vue + Ionic.
Each notification should support file uploads (for example, product images or promotional flyers).

## First Steps

Fork the repository provided for this test.
Inside your fork, create a new branch following this convention:
```
feature/<your-name>
```


Example: 
```
feature/jack-blaze
```
Work only inside your branch and commit regularly.
When finished, push your branch and make a pull request

## Technical Requirements
### Backend (Django or Python)

- Implement WebSockets (using Django Channels or any similar library).
- Allow sending notifications in JSON format with the following fields:
  - id
  - title
  - message
  - timestamp
  - type
  - file_url (optional link to the uploaded file or image)
- Provide a REST endpoint that lists all stored notifications.
- Support file uploads (images or PDFs) attached to notifications.

Example message:
```JSON
{
  "id": 1,
  "title": "New Promotion",
  "message": "Buy 3 chocolates and pay for 2!",
  "timestamp": "2025-10-18T18:00:00Z",
  "type": "promo",
  "file_url": "http://localhost:8000/uploads/choco.png"
}
```
### Frontend (Vue 3 + Ionic)

- Display a list of notifications received from the WebSocket.
- Allow viewing notification details (including the attached file or image).
- Show new notifications in real time without page reloads.
- Apply basic UX/UI design principles: clean layout, color harmony, readable typography, and clear visual hierarchy.

## Documentation (in English)

Include a short README.md file with:
- **Install:**  Steps to run the backend and frontend locally.
- **Usage:** How to open the app and see the notifications.
- **WebSocket Info:** A short note explaining how real-time messages are received.
