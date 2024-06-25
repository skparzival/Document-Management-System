Document Management System

The provided code implements a basic Document Management System using Flask, SQLAlchemy for database management, and the Python Imaging Library (PIL) for handling image files. Below is a brief documentation explaining its design and usage:

Components and Functionality

1. Flask Application Setup:
   - The application is initialized using Flask with configurations set for the SQLite database (`documents.db`) and the uploads folder (`/uploads`) where documents/files are stored.

2. Document Model (`Document`):
   - Attributes: 
     - `document_id`: Primary key for identifying documents.
     - `title`: Title of the document (max length 100).
     - `description`: Description of the document (max length 200).
     - `upload_date`: Date and time when the document was uploaded (default is current UTC time).
     - `file_path`: Path to the stored file in the uploads folder.

   - Methods:
     - `save()`: Saves the document instance to the database.
     - `delete()`: Deletes the document instance from the database and removes its associated file from the uploads folder.

3. Database Operations:
   - Uses SQLAlchemy for defining the `Document` model, creating database tables (`db.create_all()`), and performing CRUD operations (`db.session.add()`, `db.session.commit()`, `db.session.delete()`).

4. Flask Routes:
   - `/` (home): Displays all documents with links to view, update, delete, and download.
   - `/upload`: Allows uploading new documents with a title, description, and file upload.
   - `/document/<int:document_id>`: Shows details of a specific document.
   - `/update/<int:document_id>`: Allows updating title, description, and file of a document.
   - `/delete/<int:document_id>`: Deletes a document and its associated file.
   - `/download/<int:document_id>`: Allows downloading the file of a document.

5. Templates:
   - Uses HTML templates (`index.html`, `upload.html`, `view.html`, `update.html`) rendered using Jinja2 template engine to display and manage documents.

6. File Management:
   - Manages file uploads and downloads using Flask's `request.files` and `send_from_directory` for serving files.

Usage

1. Setup:
   - Install dependencies (`Flask`, `SQLAlchemy`) using `pip`.
   - Run the Flask application (`main.py`).

2. Interacting with the System:
   - Navigate to `http://localhost:5000/` in a web browser.
   - Use the provided UI to upload, view, update, delete, and download documents/files.

3. Features:
   - Secure file uploads with validation for required fields.
   - CRUD operations for managing documents.
   - Error handling for file operations and database interactions.


This Document Management System provides a basic framework for storing, managing, and accessing documents/files through a web interface. It leverages Flask for web development, SQLAlchemy for database management, and integrates file handling for uploading, downloading, and storing documents. It's suitable for scenarios where simple document management capabilities are required within a web application context.

