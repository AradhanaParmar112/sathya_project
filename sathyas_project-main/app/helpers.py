from .models import Table, Holder, Row, Report
from django.conf import settings
from django.core.mail import send_mail



def burt_helper(request):
    report_type = request.POST.get('query_select')
    
    the_report = Report()
    the_report.name = request.POST.get('report_name')
    the_report.type_of_report = report_type
    the_report.created_by = request.user
    the_report.save()

    number_of_tables = int(request.POST.get('number_of_table'))
    
    for i in range(number_of_tables):
        # single table grabbing
        table_name = request.POST.get(f'table_name_given_by_user{i}')
        row = int(request.POST.get(f'row{i}'))
        col = int(request.POST.get(f'col{i}'))
        row_head_name = request.POST.get(f'row_head_name{i}')

        # Initializig Table Object
        t = Table()
        t.name = table_name
        t.row_head_name = row_head_name
        t.save()
        
        # Adding Table Heads/Keyword
        for j in range(col):
            h = Holder()
            h.the_holder = request.POST.get(f'keyword{i}{j}')
            h.save()
            t.header.add(h)
            t.save()
        
        # Initializing Row Object
        
        # Adding Table Rows
        for j in range(row):
            r = Row()
            r.save()
            # Grabbing and saving first keyword of row
            main_keyword = request.POST.get(f'mainkeyword{i}{j}')
            h = Holder()
            h.the_holder = main_keyword
            h.save()
            r.the_row.add(h)
            r.save()

            # grabbing and saving the queries of the row
            for k in range(col):
                data = request.POST.get(f'q{i}{j}{k}')
                h = Holder()
                h.the_holder = data
                h.save()
                r.the_row.add(h)
                r.save()
            t.rows.add(r)
            t.save()
        the_report.tables.add(t)
        the_report.save()
    
    return the_report.pk


def query_runner(report_object_pk):
    the_report = Report.objects.get(pk=report_object_pk)

    
    tables = []
    outputs = []
    for table in the_report.tables.all(): 
        table_ = {}
        table_['rows'] = []
        table_['name'] = table.name  
        table_['row_head_name'] = table.row_head_name
        # grabbing headers and adding it
        temp_head = []
        for head in table.header.all():
            temp_head.append(head.the_holder)
        # print(table.header[1])
        table_['header'] = temp_head

        
        for row_item in table.rows.all():
            temp_row = []
            for i, item in zip(range(row_item.the_row.all().count()), row_item.the_row.all()):
                
                if(i==0):
                    temp_row.append(item.the_holder)
                    print(item.the_holder)
                else:
                    # print(f'check {i}')
                    # print(table_['header'][1])
                    x = send_req_get_data(item.the_holder).lower()
                    print(x)
                    outputs.append(str(x))
                    keyword_ = str(table_['header'][i-1])
                    temp_row.append(x.count(keyword_.lower()))
                    # temp_row.append(table_['header'][i-1])
                    # print(item.the_holder)
            table_['rows'].append(temp_row)
        tables.append(table_)

    return tables, outputs




def query_runner_qtest(report_object_pk):
    the_report = Report.objects.get(pk=report_object_pk)

    
    tables = []
    outputs = []
    for table in the_report.tables.all(): 
        table_ = {}
        table_['rows'] = []
        table_['name'] = table.name  
        table_['row_head_name'] = table.row_head_name
        # grabbing headers and adding it
        temp_head = []
        for head in table.header.all():
            temp_head.append(head.the_holder)
        # print(table.header[1])
        table_['header'] = temp_head

        
        for row_item in table.rows.all():
            temp_row = []
            for i, item in zip(range(row_item.the_row.all().count()), row_item.the_row.all()):
                
                if(i==0):
                    temp_row.append(item.the_holder)
                    print(item.the_holder)
                else:
                    # print(f'check {i}')
                    # print(table_['header'][1])
                    # x = send_req_get_data(item.the_holder).lower()
                    object_type = ''
                    if str(item.the_holder).startswith("'Module'"):
                        object_type = 'test-cases'
                    else:
                        object_type = 'test-runs'
                    x = qtest_request_maker(item.the_holder, object_type)
                    # print(x)
                    # outputs.append(str(x))
                    # keyword_ = str(table_['header'][i-1])
                    temp_row.append(x)
                    # temp_row.append(table_['header'][i-1])
                    # print(item.the_holder)
            table_['rows'].append(temp_row)
        tables.append(table_)

    return tables, outputs
                

def qtest_request_maker(query, object_type):
    import requests
    import json


    url = f"https://qtest.eng.netapp.com/api/v3/projects/67/search"

    payload1 = json.dumps({
        "object_type": object_type,
        "fields": ["name", "properties", "pid", "id"],
        # "query": "'Module' in 'MD-4542 PLTE' and 'Module' not in 'MD-10321 MFGTEST_MFGT' and 'Supported Models' ~ 'Dagger2' and (Type = 'Automated' or Type = 'Automation') and ('Keywords' ~ 'Dg2RegD' or ('Keywords' ~ 'Dg2HdnD' or 'Keywords' ~ 'Dg2NewD')) and 'Keywords' !~ 'Dg2RegAuT' and 'Keywords' !~ 'Dg2NewAPln' and 'Keywords' !~ 'Dg2HdnAPln' and 'Keywords' !~ 'Dg2RegAPln' and 'Keywords' !~ 'Dg2RegAuD' and 'Keywords' !~ 'Dg2HdnAuD' and 'Keywords' !~ 'Dg2NewAuD' and ('Script Path' !~ '.thpl' and 'Script Path' !~ '.py') and 'Keywords' !~ 'qohMrg'"
        "query": str(query)
    })
    headers = {
        'Authorization': 'Bearer ef78a03b-e2e9-4c92-a46c-1b29a806fa23',
        'Content-Type': 'application/json',
        'Cookie': 'qtest-8080=s15'
    }

    response = requests.request("POST", url, headers=headers, data=payload1, verify=False)
    json_obj = json.loads(response.text)
    print(json_obj)
    total = json_obj["total"]
    return total


def mixed_query_runner(report_object_pk):
    the_report = Report.objects.get(pk=report_object_pk)
    tables = []
    outputs = []
    for table in the_report.tables.all(): 
        table_ = {}
        table_['rows'] = []
        table_['name'] = table.name  
        table_['row_head_name'] = table.row_head_name
        # grabbing headers and adding it
        temp_head = []
        for head in table.header.all():
            temp_head.append(head.the_holder)
        # print(table.header[1])
        table_['header'] = temp_head

        
        for row_item in table.rows.all():
            temp_row = []
            for i, item in zip(range(row_item.the_row.all().count()), row_item.the_row.all()):
                
                if(i==0):
                    temp_row.append(item.the_holder)
                else:
                    if str(item.the_holder).startswith('/usr/'):
                        x = send_req_get_data(item.the_holder).lower()
                        outputs.append(str(x))
                        keyword_ = str(table_['header'][i-1])
                        temp_row.append(x.count(keyword_.lower()))
                    elif str(item.the_holder).startswith("'Module'") or str(item.the_holder).startswith("'Test cycle"):
                        object_type = ''
                        if str(item.the_holder).startswith("'Module'"):
                            object_type = 'test-cases'
                        else:
                            object_type = 'test-runs'
                        x = qtest_request_maker(item.the_holder, object_type)
                        temp_row.append(x)
                    else:
                        pass #jira
            table_['rows'].append(temp_row)
        tables.append(table_)

    return tables, outputs


def send_email(the_user):
    subject = 'Report'
    message = f''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [the_user.username, ]
    send_mail( subject, message, email_from, recipient_list )
    


def send_req_get_data(query):
    import paramiko

    host = "YOUR_IP_ADDRESS"
    username = "YOUR_LIMITED_USER_ACCOUNT"
    password = "YOUR_PASSWORD"

    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    _stdin, _stdout,_stderr = client.exec_command(query)
    x = _stdout.read().decode()
    client.close()
    return x