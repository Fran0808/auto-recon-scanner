import os

def generate_html_report(report_data, filepath, target):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Recon Report - {target}</title>
    <style>
        body {{
            font-family: Arial, Helvetica, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 20px;
            font-size: 14px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: #fff;
            padding: 30px;
            border: 1px solid #ddd;
            border-top: 4px solid #00509d;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        h1 {{
            color: #00296b;
            font-size: 24px;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            color: #003f88;
            font-size: 18px;
            margin-top: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f1f5f9;
            color: #333;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #fafbfc;
        }}
        .badge {{
            background-color: #e2e8f0;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 13px;
            margin: 2px;
            display: inline-block;
        }}
        .text-danger {{
            color: #d90429;
            font-weight: bold;
        }}
        a {{
            color: #00509d;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Automated Reconnaissance Report</h1>
        <p><strong>Target:</strong> {target}</p>

        <h2>1. Open Ports & Services</h2>
        <table>
            <tr><th>Port</th><th>Service</th></tr>
"""
    for port in report_data.get("open_ports", []):
        html += f"            <tr><td>{port['port']}</td><td>{port['service']}</td></tr>\n"
        
    html += """        </table>

        <h2>2. Subdomains Discovered</h2>
        <div>
"""
    for sub in report_data.get("subdomains", []):
        html += f"            <div class='badge'><a href='http://{sub}' target='_blank'>{sub}</a></div>\n"
        
    html += """        </div>

        <h2>3. Detected Technologies</h2>
        <div>
"""
    for tech in report_data.get("web_technologies", []):
        html += f"            <span class='badge'>{tech}</span>\n"
        
    html += """        </div>

        <h2>4. Hidden Directories</h2>
        <table>
            <tr><th>Status</th><th>URL</th></tr>
"""
    for d in report_data.get("directories", []):
        status = d['status']
        status_class = "text-danger" if status == "200" else ""
        html += f"            <tr><td class='{status_class}'>{status}</td><td><a href='{d['url']}' target='_blank'>{d['url']}</a></td></tr>\n"
        
    html += """        </table>
    </div>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Clean Corporate HTML Report saved to: {filepath}")
