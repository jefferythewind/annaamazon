from django.shortcuts import render
from django.http import HttpResponse
import json
from os import environ
from sqlalchemy import create_engine
from pandas import read_sql
import math
from django.contrib.auth.decorators import login_required

engine = create_engine(environ['DATABASE_URL'], echo=False).raw_connection()
# Create your views here.

@login_required
def index(request):
    col_query = read_sql("select * from all_items limit 0;", engine)
    return render(request, 'data/index.html', context={"columns":list(col_query)})

@login_required
def orders(request):
    col_query = read_sql("select * from order_items limit 0;", engine)
    return render(request, 'data/orders.html', context={"columns":list(col_query)})

@login_required
def grouped_orders(request):return render(request, 'data/grouped_orders.html', context={"columns":['asin','title','dollar_volume','num_items','avg_price']})

@login_required
def all_data(request):
    if request.is_ajax():
        where_clause = ""
        args = {
            'all':['all_items','index'],
            'oi': ['order_items','itemid'],
            'go': ["""(select 
                        asin, 
                        title,
                        sum( CAST(qnty_shipped as FLOAT) * CAST(item_price as FLOAT) ) as dollar_volume, 
                        count(*) as num_items, 
                        avg(CAST(item_price as FLOAT)) as avg_price
                    from 
                        order_items 
                    group by 
                        title, asin) grouped_orders""", 'asin']
        }
        table_name = args[request.GET.get('arg1')][0]
        pk = args[request.GET.get('arg1')][1]
        for key, value in request.GET.items():
            #print(key, value)
            if key not in ['sidx','rows','_search','nd','sord','csrfmiddlewaretoken','page','arg1']:
                where_clause += """lower(CAST("%s" AS TEXT)) LIKE '%%%s%%' and """ % (key,value)
        where_clause = where_clause.rstrip(" and ")
        
        rows = int(request.GET.get('rows'))
        page = int(request.GET.get('page'))
        sidx = request.GET.get('sidx')
        sord = request.GET.get('sord')
        search = request.GET.get('_search')
        
        if search == "true":
            #print where_clause
            count_df = read_sql("""SELECT count(*) as the_count from %s where %s;""" % (table_name, where_clause),engine)
            df = read_sql("""SELECT * from %s where %s order by "%s" %s limit %s offset %s;""" % (table_name, where_clause, sidx, sord, rows, rows*page-rows) ,engine)
        else:
            count_df = read_sql("""SELECT count(*) as the_count from %s;""" % table_name, engine)
            df = read_sql("""SELECT * from %s order by "%s" %s limit %s offset %s;""" % (table_name, sidx, sord, rows, rows*page-rows),engine)    

        columns = list(df)

        d = df.to_dict()

        rows = []
        
        for index in d[pk]:
            new_row = {'id':d[pk][index]}
            cell = []
            for column in columns:
                cell.append(d[column][index])
                    
            new_row['cell'] = cell
            rows.append(new_row)
            
        if len(df.index) > 0:
            total = math.ceil(float(count_df.iloc[0]['the_count'])/len(df.index))
        else:
            total = 0
            
        data = {
                "total":total,
                "page":page,
                "records":count_df.iloc[0]['the_count'],
                "rows":rows
                }
        
        return HttpResponse(json.dumps(data), content_type='application/json')