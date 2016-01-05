import argparse
from datetime import datetime

from flask import Flask, redirect, request, send_from_directory, render_template
import pandoc
pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

import progress

# TODO: use a better text editor with markdown features
# TODO: dynamically generate archive
# TODO: add a whole-year view (probably to the progress library)
# TODO: auto-save progress in editor regularly

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("data_store_path")
  parser.add_argument("-t", "--template", help="template file name")
  parser.add_argument("-e", "--fileext", default="md", help="file extension")
  args = parser.parse_args()

  app = Flask(__name__)
  p = progress.Progress(args.data_store_path, args.fileext)

  def get_week_string(date=None):
    week_start = progress.get_start_of_week(date_=date)
    return week_start.strftime("%Y-%m-%d")

  def get_week_as_html(date=None):
    content = p.get_week(date_=date)
    doc = pandoc.Document()
    doc.markdown = content
    content = str(doc.html)

    week_string = get_week_string(date=date)
    edit_link = "/%s/edit" % week_string

    return content, edit_link

  @app.route('/')
  def current_week():
    content, edit_link = get_week_as_html()
    return render_template('default.html', content=content, edit_link=edit_link)

  # you might not want this
  @app.route('/goals')
  def goals_page():
    doc = pandoc.Document()
    doc.markdown = p.get_file('_goals.md')
    content = unicode(str(doc.html), "utf-8")
    return render_template('default.html', content=content)

  @app.route('/archive')
  def archive_page():
    return render_template('archive.html')

  # /YYYY-MM-DD
  @app.route('/<datestring>')
  def specific_week(datestring):
      date = datetime.strptime(datestring, "%Y-%m-%d")
      content, edit_link = get_week_as_html(date=date)
      return render_template('default.html', content=content, edit_link=edit_link)

  # /YYYY-MM-DD/edit
  @app.route('/<datestring>/edit', methods=['POST', 'GET'])
  def edit_specific_week(datestring):
      date = datetime.strptime(datestring, "%Y-%m-%d")

      if request.method == 'POST':
        if request.form['content']:
          p.set_week(request.form['content'], date_=date)
        return redirect("/%s" % datestring)

      content = p.get_week(date_=date, template=args.template)
      content = '''
      <form action="" method="post" class="edit-form">
        <textarea name="content" class="edit-textarea">%s</textarea>
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

  app.run(debug=True)

if __name__ == '__main__':
  main()
