#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 09:29:37 2023

@author: alexis
"""
from flask import Flask, jsonify, request
from textblob import TextBlob

app = Flask(__name__)

@app.route("/predict", methods=['GET'])
def get_prediction():
    text = request.args.get('text')
    testimonial = TextBlob(text).sentiment.polarity
    return jsonify(polarity=testimonial)

if __name__ == '__main__':
    app.run(port=8080)  # Run the app on port 8080



