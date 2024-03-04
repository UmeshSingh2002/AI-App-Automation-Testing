from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend

def generatePieChart(pdf, pass_count, fail_count, error_count):
    data=[pass_count, fail_count, error_count]
    labels = ['Pass','Fail', 'Error']
    pie_colors=[colors.lightgreen, colors.indianred, colors.orange]
    drawing = Drawing(400, 300)

    pie = Pie()
    pie.x = 150
    pie.y = 50
    pie.width = 200
    pie.height = 200
    pie.data = data
    pie.labels = labels
    pie.slices.strokeWidth = 0.5

    for i, color in enumerate(pie_colors):
        pie.slices[i].fillColor = color

    drawing.add(pie)
    
    legend = Legend()
    legend.alignment = 'left'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=pie)
    drawing.add(legend)

    drawing.wrapOn(pdf, 50, 400)
    drawing.drawOn(pdf, 50, 400)
    
    return pdf
    

def generateReport(metrics):
    # metric = {
    #     'tester_name': f"{type(tester).__name__}",
    #     'total_tests': total_tests,
    #     'passed_tests': passed_tests,
    #     'plant_only_pass': plant_accuracy,
    #     'disease_only_pass': disease_accuracy,
    #     'test_errors': test_errors
    # }

    try:
        for metric in metrics:
            report_file = f"./generated_reports/{metric['tester_name']}.pdf"

            pdf = canvas.Canvas(report_file, pagesize=letter)
            
            data = [
                ['# Test Cases', 
                '# Passed Cases', 
                '# Failed Cases', 
                '# Error Cases',
                'Pass Rate', 
                'Fail Rate',
                'Error Rate']
            ]

            pass_count = metric['passed_tests']
            test_errors = metric['test_errors']
            fail_count = metric['total_tests'] - pass_count - test_errors
            
            total_test_cases = pass_count + fail_count + test_errors

            data.append([
                total_test_cases, 
                pass_count, 
                fail_count,
                test_errors, 
                f'{pass_count/total_test_cases:.2%}', 
                f'{fail_count/total_test_cases:.2%}',
                f'{test_errors/total_test_cases:.2%}'
            ])
        
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            table = Table(data)
            table.setStyle(table_style)

            table.wrapOn(pdf, 20, 700)
            table.drawOn(pdf, 20, 700)

            title_text = f"Automation Test Report: {metric['tester_name']}"
            pdf.setFont('Helvetica-Bold', 16)
            pdf.drawCentredString(300, 750, title_text)
            
            pdf=generatePieChart(pdf, pass_count, fail_count, test_errors)

            pdf.save()
    except Exception as error:
        print("Oops from Report Generation")
        print("The Error is",error)

