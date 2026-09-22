from weasyprint import HTML
import json

def generate_pdf(roadmap_data, filename="roadmap.pdf"):

    html_content = "<h1>AI Career Roadmap</h1>"

    for week in roadmap_data["weeks"]:
        html_content += f"<h2>Week {week['week']} - {week['focus']}</h2>"
        html_content += "<ul>"
        for topic in week["topics"]:
            html_content += f"<li>{topic}</li>"
        html_content += "</ul>"

    HTML(string=html_content).write_pdf(filename)

    return filename