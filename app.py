@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        # Récupérer les données JSON envoyées par Flutter
        data = request.json

        # Chemin absolu du logo (dans le même répertoire que l'application Flask)
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ministere.png')

        # Date actuelle pour le pied de page
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Préparer le contenu HTML avec la page de garde et les notes des élèves
        html_content = """
<html lang="ar" dir="rtl">
    <head>
       <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Noto Naskh Arabic', sans-serif;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                    line-height: 1.6;
                }}
                h1 {{
                    text-align: center;
                    font-weight: bold;
                    font-size: 24px;
                    color: #003366;
                    margin-bottom: 20px;
                }}
                h2 {{
                    font-size: 20px;
                    color: #003366;
                    margin-top: 30px;
                    margin-bottom: 15px;
                }}
                .header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 30px;
                    direction: rtl;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-bottom: 2px solid #003366;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .header img {{
                    max-width: 120px;
                    height: auto;
                }}
                .header-left {{
                    text-align: left;
                }}
                .header-center {{
                    text-align: center;
                    flex: 1;
                }}
                .header-right {{
                    text-align: right;
                }}
                .info {{
                    margin-top: 10px;
                    font-size: 16px;
                    color: #555;
                }}
                .info p {{
                    margin: 5px 0;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                    text-align: center;
                }}
                table, th, td {{
                    border: 1px solid #003366;
                    padding: 10px;
                    text-align: center;
                }}
                th {{
                    font-weight: bold;
                    background-color: #003366;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                tr:nth-child(odd) {{
                    background-color: #ffffff;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 14px;
                    color: #666;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                }}
                .page-break {{
                    page-break-before: always;
                }}
                .cover-page {{
                    text-align: center;
                    margin-top: 100px;
                }}
                .cover-page h1 {{
                    font-size: 36px;
                    color: #003366;
                    margin-bottom: 20px;
                }}
                .cover-page p {{
                    font-size: 18px;
                    color: #555;
                    margin: 10px 0;
                }}
            </style>
    </head>
    <body>
        <!-- Page de garde -->
        <div class="cover-page">
            <h1>ملف التقییم والمتابعة</h1>
            <p><strong>القسم:</strong> {className}</p>
            <p><strong>المادة:</strong> {matiereName}</p>
            <p><strong>الأستاذ:</strong> {profName}</p>
            <p><strong>المدرسة:</strong> {schoolName}</p>
        </div>

        <!-- En-tête avec le logo du ministère et le texte -->
        <div class="header page-break">
            <!-- Côté gauche : الصف, المادة, et الأستاذ -->
            <div class="header-left" dir="rtl">
                <p><strong>القسم:</strong> {className}</p>
                <p><strong>المادة:</strong> {matiereName}</p>
                <p><strong>الأستاذ:</strong> {profName}</p>
            </div>

            <!-- Centre : Titre "جدول النتائج" -->
            <div class="header-center">
                <h1> الجدول الجامع للنتائج</h1>
            </div>

            <!-- Côté droit : Logo et nom de l'école -->
            <div class="header-right" dir="rtl">
                <img src="file:///{logo_path}" alt="Logo du Ministère de l'Éducation">
                <p><strong>المدرسة:</strong> {schoolName}</p>
            </div>
        </div>

        <!-- Tableau des notes des élèves -->
        <h2>النتائج</h2>
        <table dir="rtl">
            <thead>
                <tr>
                    <th>الاسم واللقب</th>
                    {baremesHeaders}
                </tr>
            </thead>
            <tbody>
                {studentsRows}
            </tbody>
        </table>

        <!-- Tableau du nombre d'élèves ayant atteint le maximum -->
        <h2>عدد التلاميذ المحققين للتملك</h2>
        <table dir="rtl">
            <thead>
                <tr>
                    <th> </th>
                    {baremesHeaders}
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>عدد التلاميذ المحققين للتملك</td>
                    {sumCriteriaMaxPerBaremeCells}
                </tr>
            </tbody>
        </table>

        <!-- Tableau des pourcentages -->
        <h2>النسبة المئوية للتلاميذ المحققين للتملك</h2>
        <table dir="rtl">
            <thead>
                <tr>
                    <th> </th>
                    {baremesHeaders}
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>النسبة المئوية للتلاميذ المحققين للتملك</td>
                    {percentageCells}
                </tr>
            </tbody>
        </table>

        <!-- Pied de page -->
        <div class="footer" dir="rtl">
            <p>تم إنشاء هذا التقرير تلقائياً بواسطة نظام Taqyem</p>
            <p>تاريخ الطباعة: {current_date}</p>
        </div>
    </body>
</html>
""".format(
            className=data['className'],
            matiereName=data['matiereName'],
            profName=data['profName'],
            schoolName=data['schoolName'],
            logo_path=logo_path,
            baremesHeaders=''.join(['<th>{}</th>'.format(bareme['value']) for bareme in data['baremes']]),
            studentsRows=''.join([
                """
                <tr>
                    <td>{}</td>
                    {}
                </tr>
                """.format(
                    student['name'],
                    ''.join(['<td>{}</td>'.format(student['baremes'].get(bareme['id'], '( - - - )')) for bareme in data['baremes']])
                ) for student in data['students']
            ]),
            sumCriteriaMaxPerBaremeCells=''.join([
                '<td>{}</td>'.format(data['sumCriteriaMaxPerBareme'].get(bareme['id'], 0)) for bareme in data['baremes']
            ]),
            percentageCells=''.join([
                '<td>{:.2f}%</td>'.format((data['sumCriteriaMaxPerBareme'].get(bareme['id'], 0) / data['totalStudents']) * 100) for bareme in data['baremes']
            ]),
            current_date=current_date
        )

        # Générer le PDF à partir du HTML
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf()

        # Retourner le PDF en tant que réponse pour le téléchargement
        response = make_response(pdf_bytes)
        response.headers.set('Content-Disposition', 'attachment', filename='tableau_resultats.pdf')
        response.headers.set('Content-Type', 'application/pdf')

        return response

    except Exception as e:
        # Gérer les erreurs et retourner une réponse d'erreur
        return make_response(f"Erreur lors de la génération du PDF : {str(e)}", 500)
    
if __name__ == '__main__':
    app.run(debug=True)