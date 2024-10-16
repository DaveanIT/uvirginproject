from django.shortcuts import render
from usvirginisland import settings
import pyodbc
from django.http import JsonResponse

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

    # Close the database connection
    conn.close()

    # Prepare the data for the template
    data = {
        "bills": result_data1,  # Data from first stored procedure
        "status": result_data2  # Data from second stored procedure
    }

    # Render the template with the data from both stored procedures
    return render(request, "index.html", data)

    