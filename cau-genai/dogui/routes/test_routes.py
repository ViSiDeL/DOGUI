from flask import Blueprint, render_template, request, redirect, url_for, flash
import json

test_bp = Blueprint('test', __name__)

# loading test page
@test_bp.route('/test', methods=['GET'])
def assistant():
    return render_template('template-page.html')