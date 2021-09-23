from flask import Flask, render_template, request,redirect, url_for
import requests
import json
from view import getdata,insert
from datetime import datetime,time
import math


app = Flask(__name__)



@app.route('/data')
def date():
    stet = getdata()
    data = requests.get('https://gitlab.com/-/snippets/2094509/raw/master/sample_json_2.json')
    info = data.content
    data1 = json.loads(info)


    def secondsToHoursMinutesSeconds(time_value):
        try:
            return (time_value / 3600, (time_value % 3600) / 60, (time_value % 3600) % 60)
        except ZeroDivisionError:
            return (8,9,7)

    count = 0
    for i in stet[::-1]:
        count = count + 1
        if count >= 2:
            break
        #print(i)
        try:
            startt = datetime.strptime(i[1],'%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise ValueError('Incorrect data format, should be %Y-%m-%dT%H:%M:%SZ')
        try:
            endt = datetime.strptime(i[2], '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise ValueError('Incorrect data format, should be %Y-%m-%dT%H:%M:%SZ')
        if startt > endt:
            return render_template('404.html')

        start_t = startt.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_t = endt.strftime('%Y-%m-%dT%H:%M:%SZ')
        total_runtime = 0
        total_downtime = 0

        for x in data1:
            datet = datetime.strptime(x['time'], '%Y-%m-%d %H:%M:%S')
            date_time = datet.strftime('%Y-%m-%dT%H:%M:%SZ')
            if start_t <= date_time <= end_t:

                if x['runtime'] > 1021:
                    print(datet)
                    x['downtime'] = x['runtime'] - 1021
                    x['runtime'] = 1021
                total_runtime = total_runtime + x['runtime']
                total_downtime = total_downtime + x['downtime']

        #print(f'{total_runtime },{total_downtime}')
        try:
            machine_utilisation = (total_runtime) / (total_runtime + total_downtime) * 100
        except ZeroDivisionError:
            machine_utilisation = 0

        (h,m,s) = secondsToHoursMinutesSeconds(total_runtime)
        (hr,mi,se) = secondsToHoursMinutesSeconds(total_downtime)


        sh = {
            'runtime':f"{math.trunc(h)}h:{math.trunc(m)}m:{math.trunc(s)}s",
            'downtime': f"{math.trunc(hr)}h:{math.trunc(mi)}m:{math.trunc(se)}s",
            'utilisation': float('%.2f'%machine_utilisation)
            }
        json_object = json.dumps(sh,indent = 3)

        with open('def.json','w') as file:
            file.write(json_object)



    return render_template('run.html',jsonfile=json.dumps(sh,indent = 3))


@app.route('/' ,methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        insert(start_time, end_time)
        return redirect(url_for('date'))


    return render_template('index.html')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004,debug = True)

