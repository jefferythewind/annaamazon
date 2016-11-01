from django.shortcuts import render
from django.http import HttpResponse
import json
from os import environ
from sqlalchemy import create_engine, text
from pandas import read_sql
import math

engine = create_engine(environ['DATABASE_URL'], echo=False)
# Create your views here.

def index(request):
    col_query = read_sql("select * from all_items limit 0;", engine)
    return render(request, 'data/index.html', context={"columns":list(col_query)})

def all_data(request):
    if request.is_ajax():
        where_clause = ""
        for key, value in request.GET.items():
            #print(key, value)
            if key not in ['sidx','rows','_search','nd','sord','csrfmiddlewaretoken','page']:
                where_clause += """CAST("%s" AS TEXT) LIKE '%%%s%%' and """ % (key,value)
        where_clause = where_clause.rstrip(" and ")
        
        rows = int(request.GET.get('rows'))
        page = int(request.GET.get('page'))
        sidx = request.GET.get('sidx')
        sord = request.GET.get('sord')
        search = request.GET.get('_search')
        
        
         
        if search == "true":
            #print where_clause
            count_df = read_sql(text("""SELECT count(*) as the_count from all_items where %s;""" % where_clause),engine)
            df = read_sql(text("""SELECT * from all_items where %s order by "%s" %s limit %s offset %s;""" % (where_clause, sidx, sord, rows, rows*page-rows) ),engine)
        else:
            count_df = read_sql("""SELECT count(*) as the_count from all_items;""",engine)
            df = read_sql("""SELECT * from all_items order by "%s" %s limit %s offset %s;""" % (sidx, sord, rows, rows*page-rows),engine)    

        columns = list(df)

        d = df.to_dict()

        
        rows = []
        
        for index in d['index']:
            new_row = {'id':d['index'][index]}
            cell = []
            for column in columns:
                cell.append(d[column][index])
                    
            new_row['cell'] = cell
            rows.append(new_row)
        
        data = {
                "total":math.ceil(float(count_df.iloc[0]['the_count'])/len(df.index)),
                "page":page,
                "records":count_df.iloc[0]['the_count'],
                "rows":rows
                }
        
        return HttpResponse(json.dumps(data), content_type='application/json')