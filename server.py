from datetime import datetime

from flask import Flask, redirect, request, send_from_directory, render_template
import pandoc

import progress

import config

# TODO: switch to templating and make it look pretty
# TODO: use a better text editor with markdown features
# TODO: add a calendar or something to all pages for faster navigation
# TODO: add template file support so that default content is used for new weeks
# TODO: add a whole-year view (probably to the progress library)
# TODO: auto-save progress in editor regularly

app = Flask(__name__)
p = progress.Progress(config.data_store_path, config.file_ext)

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
  content = get_week_as_html()
  return render_template('default.html', content=content)

# /YYYY-MM-DD
@app.route('/<datestring>')
def specific_week(datestring):
    date = datetime.strptime(datestring, "%Y-%m-%d")
    content = get_week_as_html(date=date)
    return render_template('default.html', content=content)

# /YYYY-MM-DD/edit
@app.route('/<datestring>/edit', methods=['POST', 'GET'])
def edit_specific_week(datestring):
    date = datetime.strptime(datestring, "%Y-%m-%d")

    if request.method == 'POST':
      if request.form['content']:
        p.set_week(request.form['content'], date_=date)
      return redirect("/%s" % datestring)

    content = p.get_week(date_=date, template=config.template)
    content = '''
    <form action="" method="post" style="margin: 40px;">
      <textarea name="content" style="margin: 0px; width: 600px; height: 500px; font-size: 14pt;">%s</textarea>
      <br><br>
      <input type="submit">
    </form>
    ''' % content

    return render_template('default.html', content=content)

# so it doesn't complain
@app.route('/favicon.ico')
def favicon():
  return send_from_directory(app.root_path, 'favicon.ico',
      mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
  app.run(debug=True)