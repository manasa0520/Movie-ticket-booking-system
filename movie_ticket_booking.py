import mysql.connector,sys import datetime from mysql.connector import Error from flask import Flask, request, jsonify, render_template from random import randint  
  
app = Flask(name)  
  
@app.route('/') def renderLoginPage():     return render_template('login.html')  
  
  
@app.route('/login', methods = ['POST']) def verifyAndRenderRespective():  
  username = request.form['username']   password = request.form['password']  
  
  try:     if username == 'cashier' and password == 'cashier123':  
  
      res = runQuery('call delete_old()')       return render_template('cashier.html')  
  
     elif username == 'manager' and password == 'Password@123':  
  
      res = runQuery('call delete_old()')       return render_template('manager.html')  
  
     else:  
      return render_template('loginfail.html')   except Exception as e:  
     print(e)  
     return render_template('loginfail.html')  
  
  
# Routes for cashier  
@app.route('/getMoviesShowingOnDate', methods = ['POST'])  
def moviesOnDate():  
   date = request.form['date']  
  
  res = runQuery("SELECT DISTINCT movie_id,movie_name,type FROM movies NATURAL JOIN shows WHERE Date = '"+date+"'")  
  
   if res == []:  
    return '<h4>No Movies Showing</h4>'   else:  
     return render_template('movies.html',movies = res)  
  
  
@app.route('/getTimings', methods = ['POST']) def timingsForMovie():  
  date = request.form['date']   movieID = request.form['movieID']   movieType = request.form['type']  
  
 res = runQuery("SELECT time FROM shows WHERE Date='"+date+"' and movie_id = "+movieID+" and type ='"+movieType+"'")  
    
   list = []  
  
   for i in res:  
     list.append( (i[0], int(i[0]/100), i[0]%100 if i[0]%100 != 0 else '00' ) )  
  
   return render_template('timings.html',timings = list)   
  
  
@app.route('/getShowID', methods = ['POST']) def getShowID():  
   date = request.form['date']  
movieID = request.form['movieID'] movieType = request.form['type'] time = request.form['time']  
   res = runQuery("SELECT show_id FROM shows WHERE Date='"+date+"' and movie_id =  
"+movieID+" and type ='"+movieType+"' and time = "+time)   return jsonify({"showID" : res[0][0]})  
  
  
@app.route('/getAvailableSeats', methods = ['POST']) def getSeating():  
   showID = request.form['showID']  
  
 res = runQuery("SELECT class,no_of_seats FROM shows NATURAL JOIN halls WHERE show_id = "+showID)  
  
  totalGold = 0   totalStandard = 0  
  
  for i in res:     if i[0] == 'gold':  
   totalGold = i[1]   if i[0] == 'standard':  
       totalStandard = i[1]  
  
   res = runQuery("SELECT seat_no FROM booked_tickets WHERE show_id = "+showID)  
  
  goldSeats = []   standardSeats = []  
  
  for i in range(1, totalGold + 1):     goldSeats.append([i,'']) for i in range(1, totalStandard + 1):  
   standardSeats.append([i,''])  
  for i in res:     if i[0] > 1000:       goldSeats[ i[0] % 1000 - 1 ][1] = 'disabled'     else:  
       standardSeats[ i[0] - 1 ][1] = 'disabled'  
  
   return render_template('seating.html', goldSeats = goldSeats, standardSeats = standardSeats)  
  
  
@app.route('/getPrice', methods = ['POST']) def getPriceForClass():  
  showID = request.form['showID']   seatClass = request.form['seatClass']  
  
   res = runQuery("INSERT INTO halls VALUES(-1,'-1',-1)");  
  
   res = runQuery("DELETE FROM halls WHERE hall_id = -1")  
  
 res = runQuery("SELECT price FROM shows NATURAL JOIN price_listing WHERE show_id = "+showID)  
  
   if res == []:  
     return '<h5>Prices Have Not Been Assigned To This Show, Please Try Again Later!</h5>'  
  
  price = int(res[0][0])   if seatClass == 'gold':  
     price = price * 1.5  
  
return '<h5>Ticket Price: $ '+str(price)+'</h5>\  
<button onclick="confirmBooking()" class="btn-warning">Confirm Booking</button>'
