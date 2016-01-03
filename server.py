from datetime import datetime

from flask import Flask
import pandoc

import progress

app = Flask(__name__)
p = progress.Progress("data/", file_ext="md")

pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

def get_week_as_html(date=None):
  content = p.get_week(date_=date)
  doc = pandoc.Document()
  doc.markdown = content
  return str(doc.html)

@app.route('/')
def current_week():
    return get_week_as_html()

# /YYYY-MM-DD
@app.route('/<datestring>')
def specific_week(datestring):
    date = datetime.strptime(datestring, "%Y-%m-%d")
    return get_week_as_html(date=date)

if __name__ == '__main__':
  app.run(debug=True)