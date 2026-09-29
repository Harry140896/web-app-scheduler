from flask import Flask,render_template, request

app=Flask(__name__)

@app.route('/')
def routes():
    return "Thank you for visiting the scheduler app."



@app.route('/create_scheduler', methods = ['GET','POST'])
def create_scheduler():
    if request.method == 'GET':
        return render_template('create_scheduler.html')
    elif request.method == 'POST':
        scheduler_name = request.form['scheduler_name']
        print(f"Scheduler '{scheduler_name}' created successfully!")
        return f"Scheduler '{scheduler_name}' created successfully!"


if __name__=="__main__":
    app.run(debug=True)    