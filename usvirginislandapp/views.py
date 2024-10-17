from django.shortcuts import render
from usvirginisland import settings
import pyodbc
from django.http import JsonResponse
from django.db import connection

# Create your views here.
def index(request):
    # Establish the connection to the database
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + settings.DATABASES['default']['HOST'] +
        ";DATABASE=" + settings.DATABASES['default']['NAME'] +
        ";UID=" + settings.DATABASES['default']['USER'] +
        ";PWD=" + settings.DATABASES['default']['PASSWORD'] + ";"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute the first stored procedure (usp_BTS_PageLoad 1)
    cursor.execute("EXEC usp_BTS_PageLoad 1")
    result1 = cursor.fetchall()
    columns1 = [column[0] for column in cursor.description]  # Get column names for result1
    result_data1 = [dict(zip(columns1, row)) for row in result1]  # Convert the result into dictionaries

    # Execute the second stored procedure (usp_BTS_PageLoad 2)
    cursor.execute("EXEC usp_BTS_PageLoad 2")
    result2 = cursor.fetchall()
    columns2 = [column[0] for column in cursor.description]  # Get column names for result2
    result_data2 = [dict(zip(columns2, row)) for row in result2]  # Convert the result into dictionaries

     # Execute the third stored procedure (usp_BTS_PageLoad 2)
    cursor.execute("EXEC usp_BTS_PageLoad_Member 1")
    result3 = cursor.fetchall()
    columns3 = [column[0] for column in cursor.description]  # Get column names for result2
    result_data3 = [dict(zip(columns3, row)) for row in result3]  # Convert the result into dictionaries

     # Execute the third stored procedure (usp_BTS_PageLoad 2)
    cursor.execute("EXEC usp_BTS_PageLoad_Member 2")
    result4 = cursor.fetchall()
    columns4 = [column[0] for column in cursor.description]  # Get column names for result2
    result_data4 = [dict(zip(columns4, row)) for row in result4]  # Convert the result into dictionaries

    # Close the database connection
    conn.close()

    # Prepare the data for the template
    data = {
        "bills": result_data1,  # Data from first stored procedure
        "status": result_data2,  # Data from second stored procedure
        "member": result_data3,
        "memberstatus": result_data4
    }

    # Render the template with the data from both stored procedures
    return render(request, "index.html", data)

def sponsorpopup(request):
    # Fetch SpNos from the request (passed from HTML)
    SpNos = request.GET.get('SpNos')
    print('Number',SpNos)
    
    param2 = 'S'  # Static value 'S'
    
    if SpNos:  # Ensure SpNos is provided
        with connection.cursor() as cursor:
            # Map SpNos to the DocEntry field in your database
            cursor.execute("EXEC usp_BTS_SponList %s, %s", [SpNos, param2])
            result = cursor.fetchall()
            print(result)
        # Return the result in JSON format
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'SpNos parameter is missing.'}, status=400)

def cosponsorpopup(request):
    # Fetch SpNos from the request (passed from HTML)
    CoSpNos = request.GET.get('CoSpNos')
    print('Number',CoSpNos)
    
    param2 = 'C'  # Static value 'C'
    
    if CoSpNos:  # Ensure SpNos is provided
        with connection.cursor() as cursor:
            # Map SpNos to the DocEntry field in your database
            cursor.execute("EXEC usp_BTS_SponList %s, %s", [CoSpNos, param2])
            result = cursor.fetchall()
            print(result)
        # Return the result in JSON format
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'SpNos parameter is missing.'}, status=400)


