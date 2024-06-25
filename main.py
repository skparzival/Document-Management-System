'''Document Management System'''

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application
app = Flask(__name__)
# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Class Document for defining the document model
class Document(db.Model):
    '''Defining the Document model'''
    document_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    file_path = db.Column(db.String(200), nullable=False)

    def save(self):
        '''Save the document instance to the database'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''Delete the document instance from the database and its associated file'''
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    '''Main page routing of the Document management system'''
    documents = Document.query.all()
    return render_template('index.html', documents=documents)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    '''Upload document page routing'''
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        if not title or not description or not file:
            return "All fields are required", 400
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            new_document = Document(title=title, description=description, file_path=file_path)
            db.session.add(new_document)
            db.session.commit()
            return redirect('/')
        except FileNotFoundError as e:
            return str(e), 500
    return render_template('upload.html')

@app.route('/document/<int:document_id>')
def view_document(document_id):
    '''View document page routing'''
    document = Document.query.get_or_404(document_id)
    return render_template('view.html', document=document)

@app.route('/update/<int:document_id>', methods=['GET', 'POST'])
def update_document(document_id):
    '''Update document details page routing'''
    document = Document.query.get_or_404(document_id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        if not title or not description:
            return "Title and description are required", 400
        document.title = title
        document.description = description
        file = request.files['file']
        if file:
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                document.file_path = file_path
            except FileNotFoundError as e:
                return str(e), 500
        db.session.commit()
        return redirect(url_for('view_document', document_id=document.document_id))
    return render_template('update.html', document=document)

@app.route('/delete/<int:document_id>', methods=['POST'])
def delete_document(document_id):
    '''Delete document routing'''
    document = Document.query.get_or_404(document_id)
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    db.session.delete(document)
    db.session.commit()
    return redirect('/')

@app.route('/download/<int:document_id>')
def download_document(document_id):
    '''Download document routing'''
    document = Document.query.get_or_404(document_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(document.file_path))

if __name__ == '__main__':
    app.run(debug=True)
