from datetime import datetime

from flask import Flask, redirect, request
import pandoc

import progress

app = Flask(__name__)
p = progress.Progress("data/", file_ext="md")

pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

def get_week_string(date=None):
  week_start = progress.get_start_of_week(date_=date)
  return week_start.strftime("%Y-%m-%d")

def get_week_as_html(date=None):
  content = p.get_week(date_=date)
  doc = pandoc.Document()
  doc.markdown = content
  content = str(doc.html)

  week_string = get_week_string(date=date)
  content += '\n\n <a href="%s/edit">Edit</a>' % week_string

  return content

@app.route('/')
def current_week():
    return get_week_as_html()

# /YYYY-MM-DD
@app.route('/<datestring>')
def specific_week(datestring):
    date = datetime.strptime(datestring, "%Y-%m-%d")
    return get_week_as_html(date=date)

# /YYYY-MM-DD/edit
@app.route('/<datestring>/edit', methods=['POST', 'GET'])
def edit_specific_week(datestring):
    date = datetime.strptime(datestring, "%Y-%m-%d")

    if request.method == 'POST':
      if request.form['content']:
        p.set_week(request.form['content'], date_=date)

      return redirect("/%s" % datestring)

    content = p.get_week(date_=date)

    return '''
    <form action="" method="post">
      <textarea name="content" style="margin: 0px; width: 600px; height: 500px;">%s</textarea>
      <br><br>
      <input type="submit">
    </form>
    ''' % content

if __name__ == '__main__':
  app.run(debug=True)