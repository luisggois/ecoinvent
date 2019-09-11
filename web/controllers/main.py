from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from web.models.dataset import Dataset
from .forms.form_search import SearchForm
from web import db
import xml.etree.ElementTree as ET
import json

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@login_required
def home():
    return render_template("index.html")


def allowed_file(filename):
    return filename.lower().endswith(current_app.config['ALLOWED_EXTENSIONS'])


@main.route('/upload', methods=['POST'])
@login_required
def upload():

    try:

        if 'file' not in request.files or not all(element in request.headers for element in ['Version', 'Model']):
            return "Not all necessary elements were provided!", 412

        file = request.files['file']
        version = request.headers['Version']
        model = request.headers['Model']

        if not allowed_file(file.filename):
            return 'File upload is not allowed, extension is not supported!', 412

        tree = ET.parse(file)
        root = tree.getroot()
        prefix = "{http://www.EcoInvent.org/EcoSpold02}"

        tags = {elem.tag for elem in tree.iter()}
        activity_dataset = root.find(f'{prefix}activityDataset')

        activity_description = activity_dataset.find(f'{prefix}activityDescription')
        flow_data = activity_dataset.find(f'{prefix}flowData')

        activity = activity_description.find(f'{prefix}activity')
        activity_name = activity.find(f'{prefix}activityName').text

        geography = activity_description.find(f'{prefix}geography')
        geography_name = geography.find(f'{prefix}shortname').text

        intermediate_exchanges = flow_data.findall(f'{prefix}intermediateExchange')
        reference_products = [exchange.find(f'{prefix}name').text for exchange in intermediate_exchanges
                              if exchange.find(f'{prefix}outputGroup').text == str(0)]

        reference_product = sorted(reference_products)[0]

        dataset = Dataset(version=version, model=model, activity_name=activity_name, geography_name=geography_name,
                          reference_product_name=reference_product, user_id=current_user.id)
        db.session.add(dataset)
        db.session.commit()

        return '', 204

    except:

        return 'Unexpected error!', 500


@main.route('/datasets', methods=['GET', 'POST'])
@login_required
def datasets():

    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    if form.validate_on_submit():
        kwargs = {f'{form.field.data}': f'{form.value.data.lower()}'}
        datasets = Dataset.query.filter_by(user_id=current_user.id, **kwargs).order_by(Dataset.id.desc()).paginate(page=page, per_page=5)
        if not datasets.items:
            flash('No results found!', 'warning')
        return render_template("datasets.html", datasets=datasets, form=form)

    datasets = Dataset.query.filter_by(user_id=current_user.id).order_by(Dataset.id.desc()).paginate(page=page, per_page=5)
    if not datasets.items:
        flash('No results found!', 'warning')
    return render_template("datasets.html", datasets=datasets, form=form)


@main.route("/dataset/<int:dataset_id>/delete", methods=['DELETE'])
@login_required
def delete_dataset(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    if dataset.by != current_user:
        abort(403)
    db.session.delete(dataset)
    db.session.commit()
    flash('Dataset has been deleted!', 'success')
    return redirect(url_for('main.datasets'))
