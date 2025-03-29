from flask import Flask, request, make_response
from flask_cors import CORS
import os
from datetime import datetime
import base64

app = Flask(__name__)
CORS(app)

@app.route('/generate-html-report', methods=['POST'])
def generate_html_report():
    try:
        # Récupérer les données JSON
        data = request.json

        # Encoder le logo en base64
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ministere.png')
        logo_base64 = ""
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Date actuelle
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Génération des en-têtes de colonnes
        baremes_headers = ''.join([f'<th>{bareme["value"]}</th>' for bareme in data['baremes']])
        
        # Génération des lignes d'élèves
        students_rows = ''
        for student in data['students']:
            cells = ''.join([f'<td>{student["baremes"].get(bareme["id"], "( - - - )")}</td>' 
                           for bareme in data['baremes']])
            students_rows += f'<tr><td>{student["name"]}</td>{cells}</tr>'
        
        # Génération des statistiques
        sum_cells = ''.join([f'<td>{data["sumCriteriaMaxPerBareme"].get(bareme["id"], 0)}</td>' 
                           for bareme in data['baremes']])
        
        percentage_cells = ''.join([f'<td>{((data["sumCriteriaMaxPerBareme"].get(bareme["id"], 0) / data["totalStudents"]) * 100):.2f}%</td>' 
                                  for bareme in data['baremes']])

            # Construction du HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير النتائج</title>
    <style>
        /* Styles de base */
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            color: #333;
        }}
        
        .container {{
            max-width: 100%;
            margin: 0 auto;
            padding: 15px;
        }}
        
        /* Style pour l'en-tête horizontal */
        .header {{
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid #075260;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .header-info {{
            flex: 1;
            min-width: 200px;
            text-align: right;
        }}
        
        .header-title {{
            flex: 2;
            text-align: center;
        }}
        
        .header-logo {{
            flex: 1;
            min-width: 150px;
            text-align: left;
        }}
        
        .header-text {{
            margin: 3px 0;
            font-size: 14px;
        }}
        
        .logo {{
            height: 60px;
            max-width: 100%;
            object-fit: contain;
        }}
        
        /* Tableaux */
        .table-container {{
            width: 100%;
            overflow-x: auto;
            margin: 15px 0;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        
        th, td {{
            border: 1px solid #075260;
            padding: 6px 8px;
            text-align: center;
        }}
        
        th {{
            background-color: #075260;
            color: white;
            font-weight: bold;
        }}
        
        /* Bouton d'impression */
        .print-btn {{
            position: fixed;
            top: 10px;
            left: 10px;
            padding: 8px 15px;
            background-color: #075260;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            z-index: 1000;
            font-size: 14px;
        }}
        
        /* Styles pour impression */
        @media print {{
            @page {{
                size: A4;
                margin: 10mm;
            }}
            
            body {{
                padding: 0;
                background-color: white;
                font-size: 11pt;
            }}
            
            .print-btn {{
                display: none;
            }}
            
            table {{
                page-break-inside: auto;
            }}
            
            tr {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">طباعة التقرير</button>

    <div class="container">
        <!-- En-tête horizontal -->
        <div class="header">
            <div class="header-info">
                <p class="header-text"><strong>الأستاذ:</strong> {data['profName']}</p>
                <p class="header-text"><strong>المادة:</strong> {data['matiereName']}</p>
                <p class="header-text"><strong>القسم:</strong> {data['className']}</p>
            </div>
            
            <div class="header-title">
                <h2 style="margin:0;color:#075260;">الجدول الجامع للنتائج</h2>
            </div>
            
            <div class="header-logo">
                {f'<img src="data:image/png;base64,{logo_base64}" class="logo" alt="شعار الوزارة">' if logo_base64 else ''}
                <p class="header-text"><strong>المؤسسة:</strong> {data['schoolName']}</p>
            </div>
        </div>
        
        <!-- Tableau principal -->
        <div class="table-container">
            <table dir="rtl">
                <thead>
                    <tr>
                        <th>الاسم واللقب</th>
                        {baremes_headers}
                    </tr>
                </thead>
                <tbody>
                    {students_rows}
                    
                    <!-- Ligne des statistiques -->
                    <tr style="background-color: #e9ecef;">
                        <td><strong>عدد التلاميذ المحققين</strong></td>
                        {sum_cells}
                    </tr>
                    
                    <!-- Ligne des pourcentages -->
                    <tr style="background-color: #e9ecef;">
                        <td><strong>النسبة المئوية</strong></td>
                        {percentage_cells}
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Pied de page -->
        <div style="text-align: center; margin-top: 15px; font-size: 12px;">
            <p>تم إنشاء التقرير بواسطة نظام تقييم - {current_date}</p>
        </div>
    </div>
</body>
</html>
"""
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response

    except Exception as e:
        return make_response(f"Erreur lors de la génération du rapport: {str(e)}", 500)

if __name__ == "__main__":
    app.run()