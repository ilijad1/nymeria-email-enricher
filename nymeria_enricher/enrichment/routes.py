import os
import sys

import pyexcel as pe
from flask import Blueprint, after_this_request, current_app, flash, jsonify, render_template, request, \
    send_from_directory, url_for
from flask_login import login_required
from pyexcel.exceptions import FileTypeNotSupported
from werkzeug.utils import redirect, secure_filename

from nymeria_enricher import Config
from nymeria_enricher.enrichment.nymeria_utls import get_email

csv_enrich_blueprint = Blueprint('csv_enrich', __name__)

ALLOWED_EXTENSIONS = {'csv', 'csvz', 'tsv' 'xlsx', 'xlsm', 'ods'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True


@csv_enrich_blueprint.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('upload_form.html')


@csv_enrich_blueprint.route("/upload/csv", methods=['POST'])
@login_required
def upload_csv():
    if request.method == 'POST' and 'excel' in request.files:
        # handle file upload
        filename = request.files['excel'].filename
        extension = filename.split(".")[-1]
        content = request.files['excel'].read()
        f = request.files['excel']

        file = request.files['excel']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unparsed_file = os.path.join(Config.UPLOAD_UNPARSED_CSV_PATH, filename)
            file.save(unparsed_file)

        # if sys.version_info[0] > 2:
        #     content = content.decode('utf-8')

        try:
            sheet = pe.get_sheet(file_type=extension, file_content=content)
        except FileTypeNotSupported:
            flash('Invalid file format, please stick to the supported types...', 'danger')
            return render_template('upload_form.html')

        sheet.name_columns_by_row(0)

        json_cnt = jsonify({"result": sheet.dict})
        json = json_cnt.json["result"]

        if (is_json_key_present(json, "linkedinUrl") and is_json_key_present(json, "email")):
            linkedin_urls = json["linkedinUrl"]
            emails = json["email"]
            _emails = []

            for l_url, email in zip(linkedin_urls, emails):
                if email in ['', "", " ", ' ', None] and l_url not in ['', "", " ", ' ', None]:
                    email = get_email(l_url)
                    _emails.append(email)
                else:
                    _emails.append("")
            json["email"] = _emails
        else:
            flash('Invalid column names, please set them as expected... Missing linkedinUrl or email columns', 'danger')
            return render_template('upload_form.html')

        sheet_parsed = pe.get_sheet(adict=json)
        sheet_parsed.save_as(os.path.join(Config.UPLOAD_PARSED_CSV_PATH, filename))

        return send_from_directory(directory=Config.UPLOAD_PARSED_CSV_PATH, filename=filename, as_attachment=True)

    flash('Please Upload File', 'danger')
    return render_template('upload_form.html')
