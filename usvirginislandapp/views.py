from django.shortcuts import render
from usvirginisland import settings
import pyodbc
from django.http import JsonResponse
from django.db import connection

# Create your views here.
def index(request):
    data = {
        "bills": None,  # Data from first stored procedure
        "status": None,  # Data from second stored procedure
        "member": None,
        "memberstatus": None
    }
    if request.method == 'POST':
        leg_no = request.POST.get('legno', 'n')  # Default to 'n' if unchecked
        approved = request.POST.get('approved', 'n')  # Default to 'n' if unchecked
        vetoed = request.POST.get('vetoed', 'n')  # Default to 'n' if unchecked
        ovrd = request.POST.get('overrdn', 'n')  # Default to 'n' if unchecked
        assigned = request.POST.get('toassgnd', 'n')  # Default to 'n' if unchecked
        intro = request.POST.get('tointro', 'n')  # Default to 'n' if unchecked
        senator = request.POST.get('tosnt', 'n')  # Default to 'n' if unchecked
        prim_spon = request.POST.get('primspon', 'n')  # Default to 'n' if unchecked
        to_gov = request.POST.get('togov', 'n')  # Default to 'n' if unchecked
        to_lt_gov = request.POST.get('toltgov', 'n')  # Default to 'n' if unchecked
        from_dt = request.POST.get('fromdate', 'n')  # Default to 'n' if unchecked
        to_dt = request.POST.get('todate', 'n')  # Default to 'n' if unchecked
        billno = request.POST.get('billnum', 'n')  # Default to 'n' if unchecked
        actnum = request.POST.get('actno', 'n')  # Default to 'n' if unchecked
        brno = request.POST.get('brno', 'n')  # Default to 'n' if unchecked
        amnno = request.POST.get('amnno', 'n')  # Default to 'n' if unchecked
        resono = request.POST.get('resono', 'n')  # Default to 'n' if unchecked
        goverrno = request.POST.get('govrrno', 'n')  # Default to 'n' if unchecked
        print(f"Legislature No: {leg_no}")
        print(f"Approved: {approved}")
        print(f"Vetoed: {vetoed}")
        print(f"Overridden: {ovrd}")
        print(f"Assigned: {assigned}")
        print(f"Introduced: {intro}")
        print(f"To Senator: {senator}")
        print(f"Primary Sponsor: {prim_spon}")
        print(f"To Governor: {to_gov}")
        print(f"To Lt. Governor: {to_lt_gov}")
        print(f"From Date: {from_dt}")
        print(f"To Date: {to_dt}")
        print(f"Bill No: {billno}")
        print(f"Act No: {actnum}")
        print(f"BR No: {brno}")
        print(f"Amendment No: {amnno}")
        print(f"Resolution No: {resono}")
        print(f"Governor No: {goverrno}")
        
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

        cursor.execute("""
            EXEC [dbo].[usp_BTS_PageLoad]
            @QryId = ?,
            @PageLoad = ?,
            @LegNum = ?,
            @Appr = ?,
            @Vetod = ?,
            @Ovrd = ?,
            @Assn = ?,
            @Intro = ?,
            @Sent = ?,
            @Govr = ?,
            @Ltgov = ?,
            @FromDt = ?,
            @ToDt = ?,
            @BilNo = ?,
            @ActNo = ?,
            @BRNo = ?,
            @AmndNo = ?,
            @ResoNo = ?,
            @GovNo = ?,
            @TNo = ?;
        """,1,'N',leg_no,approved,vetoed,ovrd,assigned,intro,senator,to_gov,to_lt_gov,from_dt,to_dt,billno,actnum,brno,amnno,resono,goverrno,'')

        result1 = cursor.fetchall()
        columns1 = [column[0] for column in cursor.description]
        result_data1 = [dict(zip(columns1, row)) for row in result1]# Convert the result into dictionaries

        cursor.execute("""
            EXEC [dbo].[usp_BTS_PageLoad]
            @QryId = ?,
            @PageLoad = ?,
            @LegNum = ?,
            @Appr = ?,
            @Vetod = ?,
            @Ovrd = ?,
            @Assn = ?,
            @Intro = ?,
            @Sent = ?,
            @Govr = ?,
            @Ltgov = ?,
            @FromDt = ?,
            @ToDt = ?,
            @BilNo = ?,
            @ActNo = ?,
            @BRNo = ?,
            @AmndNo = ?,
            @ResoNo = ?,
            @GovNo = ?,
            @TNo = ?;
        """,2,'n',leg_no,approved,vetoed,ovrd,assigned,intro,senator,to_gov,to_lt_gov,from_dt,to_dt,billno,actnum,brno,amnno,resono,goverrno,'')

        result2 = cursor.fetchall()
        columns2 = [column[0] for column in cursor.description]
        result_data2 = [dict(zip(columns2, row)) for row in result2]# Convert the result into dictionaries
        data = {
            "bills": result_data1,  # Data from first stored procedure
            "status": result_data2,  # Data from second stored procedure
            "member": None,
            "memberstatus": None
        }
        print("result_data2")
        print(result_data2)

        

    else:  # Handle the GET request
        try:
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

            # Define the parameters for the stored procedure
            params = (1, 'Y', None, None, None, None, None, None, None, 
                      None, None, None, None, None, None, None, None, None,None, None)

            # Execute the stored procedure with parameters
            cursor.execute("""
                EXEC [dbo].[usp_BTS_PageLoad]
                @QryId = ?,
                @PageLoad = ?,
                @LegNum = ?,
                @Appr = ?,
                @Vetod = ?,
                @Ovrd = ?,
                @Assn = ?,
                @Intro = ?,
                @Sent = ?,
                @Govr = ?,
                @Ltgov = ?,
                @FromDt = ?,
                @ToDt = ?,
                @BilNo = ?,
                @ActNo = ?,
                @BRNo = ?,
                @AmndNo = ?,
                @ResoNo = ?,
                @GovNo = ?,
                @TNo = ?;
            """, params)

            result1 = cursor.fetchall()
            columns1 = [column[0] for column in cursor.description]
            result_data1 = [dict(zip(columns1, row)) for row in result1]# Convert the result into dictionaries

            # Execute the second stored procedure (usp_BTS_PageLoad 2)
            # cursor.execute("EXEC usp_BTS_PageLoad 2")

            # Define the parameters for the stored procedure
            params = (2, 'Y', None, None, None, None, None, None, None, 
                      None, None, None, None, None, None, None, None, None,None, None)

            # Execute the stored procedure with parameters
            cursor.execute("""
                EXEC [dbo].[usp_BTS_PageLoad]
                @QryId = ?,
                @PageLoad = ?,
                @LegNum = ?,
                @Appr = ?,
                @Vetod = ?,
                @Ovrd = ?,
                @Assn = ?,
                @Intro = ?,
                @Sent = ?,
                @Govr = ?,
                @Ltgov = ?,
                @FromDt = ?,
                @ToDt = ?,
                @BilNo = ?,
                @ActNo = ?,
                @BRNo = ?,
                @AmndNo = ?,
                @ResoNo = ?,
                @GovNo = ?,
                @TNo = ?;
            """, params)
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
                "bills": result_data1 ,# Data from first stored procedure
                "status": result_data2,  # Data from second stored procedure
                "member": result_data3,
                "memberstatus": result_data4
            }
        except pyodbc.Error as e:
            print(f"Database error: {e}")
    
    # Render the template with the data from the stored procedure
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


