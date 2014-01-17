# Copyright (C) 2014 Abhay Vardhan. All Rights Reserved.
"""
Author: abhay.vardhan@gmail.com
 main.py is the top level script.
"""

from globals import app
import api_server
import search_index


@app.route('/build-index')
def buildIndex():
    """
    This request is called from cron daily to refresh the index
    :return:
    """
    search_index.build()
    return 'ok'