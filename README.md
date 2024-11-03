# TaskPilot - Project Management Web Application

**Bachelor's Thesis by Bogdan Ivan**  
University of Bucharest, Faculty of Mathematics and Computer Science  
Advisor: Assoc. Prof. Radu-Eugen Boriga, PhD  
Date: June 2024

## Overview

**TaskPilot** is an innovative project management platform that integrates a virtual project manager chatbot, powered by artificial intelligence, to facilitate team communication and coordination. Designed with simplicity in mind, TaskPilot enables teams to optimize project management processes, focus on technical and creative tasks, and maintain productivity across various working setups (physical, hybrid, or remote).

## Features

- **AI-Powered Chatbot**: TaskPilot’s virtual assistant provides real-time responses to questions about development methodologies and project-specific details, helping teams focus on execution.
- **Microservices Architecture**: Modular and scalable design to enhance performance, reliability, and flexibility.
- **User-Friendly Interface**: Simple and intuitive interface built with NiceGUI, making it accessible for users of varying technical experience.
- **Comprehensive Project Management**: Task organization into tickets (Epics, Stories, Tasks, and Bugs) and efficient tracking of priorities and statuses.
- **Docker Containerization**: Ensures consistency across development and production environments.

## Technology Stack

- **Backend**: FastAPI
- **Frontend**: NiceGUI
- **Database**: Elasticsearch
- **AI Integration**: OpenAI API
- **Containerization**: Docker

## Project Structure

- **User Management**: Authentication, role-based access control, and secure password storage.
- **Project Management**: Create, modify, and track projects with member associations.
- **Ticketing System**: Define tasks within projects, assign priority and status, and track progress.
- **Commenting System**: Users can provide additional context and updates on tasks through comments.

## Architecture

TaskPilot follows a microservices-based architecture with separate services for the frontend (UI), backend (API) and database (Elasticsearch). This architecture supports horizontal scalability and allows each component to be developed, deployed, and maintained independently.

## Installation and Deployment

### Prerequisites

- **Docker**: For containerized deployment
- **Python 3.8+**
- **FastAPI and NiceGUI** dependencies (see `requirements.txt`)

### Steps to Run Locally

1. **Clone the Repository**:
    ```bash
    git clone <repo-url>
    cd <repo-directory>
    ```

2. **Build and Run the Application**:
    Run the following command to build and start the Docker containers:
    ```bash
    sh build_runner.sh
    ```

3. **Access the Application**:
    Open a web browser and go to `http://localhost:8081` to start using TaskPilot.

## Future Development

- **Enhanced AI Capabilities**: Further refinement of the chatbot to support more complex queries and project management strategies.
- **Extended User Roles**: Introducing more granular roles and permissions within project teams.
- **Scalability Enhancements**: Implementing Kubernetes for container orchestration in larger deployments.

## Screenshots

For screenshots and detailed diagrams, please refer to the appendix of the [bachelor's thesis](https://github.com/bogdanivan12/TaskPilot/blob/main/Licenta_Ivan_Bogdan.pdf).

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

For more details on the project, refer to the complete [thesis documentation](https://github.com/bogdanivan12/TaskPilot/blob/main/Licenta_Ivan_Bogdan.pdf).
