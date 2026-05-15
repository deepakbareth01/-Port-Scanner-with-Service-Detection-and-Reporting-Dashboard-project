from flask import Flask, render_template, request, send_file
from scanner import scan_target
from database import init_db, save_scan, get_all_scans
from reporter import export_csv, export_pdf

app = Flask(__name__)
init_db()

# Store latest scan in memory for export
latest_results = []
latest_target = ""


@app.route('/', methods=['GET', 'POST'])
def index():
    global latest_results, latest_target

    if request.method == 'POST':
        target = request.form['target']
        start_port = int(request.form.get('start_port', 1))
        end_port = int(request.form.get('end_port', 1024))

        results = scan_target(target, start_port, end_port)

        latest_results = results
        latest_target = target

        save_scan(target, results)

        return render_template(
            'results.html',
            target=target,
            results=results,
            total=len(results)
        )

    return render_template('index.html')


@app.route('/history')
def history():
    scans = get_all_scans()
    return render_template('history.html', scans=scans)


@app.route('/export/csv')
def export_csv_route():
    if not latest_results:
        return 'No scan data available.'

    export_csv(latest_results)
    return send_file('scan_report.csv', as_attachment=True)


@app.route('/export/pdf')
def export_pdf_route():
    if not latest_results:
        return 'No scan data available.'

    export_pdf(latest_results)
    return send_file('scan_report.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=8000)