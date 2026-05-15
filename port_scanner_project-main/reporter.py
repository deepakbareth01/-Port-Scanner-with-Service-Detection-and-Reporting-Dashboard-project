import csv
from fpdf import FPDF



def export_csv(results, filename="scan_report.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Service", "Banner"])

        for item in results:
            writer.writerow([
                item["port"],
                item["service"],
                item["banner"],
            ])



def export_pdf(results, filename="scan_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, text="Port Scan Report", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    for item in results:
        line = (
            f"Port {item['port']} | "
            f"Service: {item['service']} | "
            f"Banner: {item['banner'][:60]}"
        )
        pdf.multi_cell(0, 8, line)

    pdf.output(filename)