# README

## Project Overview
The **AR Platform Master** project is a Python-based application designed to run a server using Flask. It integrates Firebase for backend functionality and provides a database schema to manage application data.

## Project Structure
The project is organized as follows:

- **`ar_server/`**: Contains the core application code for the Flask server.
- **`images/`**: Stores images used in the project.
- **`old/`**: Potentially contains legacy or backup files.
- **`server_conf/`**: Configuration files for the server.
- **`setup.py`**: Script for packaging and installing the application.
- **`Makefile`**: Includes various commands for managing the project lifecycle.
- **`MANIFEST.in`**: Specifies additional files to include in the package.

## Installation
Follow these steps to set up and run the project:

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd ar_platform-master
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -e .
   ```

4. **Initialize the Database:**
   ```bash
   export FLASK_APP=ar_server
   export FLASK_ENV=development
   flask init-db
   ```

5. **Run the Application:**
   ```bash
   flask run
   ```

## Web Application Setup
To set up and access the web application, follow these additional steps:

1. **Configure the Server:**
   - Modify the configuration files located in `server_conf/` as needed for your environment.
   - Ensure the Firebase credentials file is placed in a secure directory and referenced correctly in the application.

2. **Access the Web Interface:**
   - Once the server is running, open a web browser and navigate to:
     ```
     https://localhost:5000
     ```

3. **Test the Application:**
   - Use the provided endpoints or the graphical interface to verify that the application functions as expected.

4. **Deployment:**
   - For production deployment, configure a production-ready server (e.g., Gunicorn or uWSGI) and set up HTTPS with a valid SSL certificate.
   - Update environment variables and configurations as required for production.

## Usage
- To start the server in debug mode with HTTPS:
  ```bash
  make run
  ```

- To initialize the database:
  ```bash
  make init
  ```

- To explore the database directly:
  ```bash
  make explore_db
  ```

## File Inclusions
The following are included in the project package:
- SQL schema: `ar_server/schema.sql`
- Static files: `ar_server/static/`
- Templates: `ar_server/templates/`

## Dependencies
The project requires the following Python packages:
- `flask`
- `firebase-admin`
- `jsonschema`

## Contributing
To contribute to this project:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## License
This project is licensed under the CC-BY-SA License. See the LICENSE file for more details.

