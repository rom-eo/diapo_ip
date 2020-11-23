from flask import Flask
from flask import render_template
from flask import request, session,redirect, url_for,send_file
from werkzeug.utils import secure_filename
import glob
import os

app = Flask(__name__)
app.secret_key = 'your key here'

@app.route('/')
def hello():
    return '''
<h1> Welcome to Diapo Over Ip!</h1>
<a href="/diapo/example">Visite a room</a>
</br>
<a href="/diapo_admin">Admin Account</a>
</br>
<a href="/diapo_admin_login">Admin login</a>


'''

 

@app.route('/diapo/<path:room>', methods=['POST', 'GET'])
def diapo1(room):
    
    a=glob.glob("./static/rooms/"+room)
    if len(a)!=1:
        return "room not found"+'</br> <a href="/diapo_admin_login'+'">Create it </a>'
    Apath="./static/rooms/"+room
    aFile=open(Apath+'/params/sel.txt','r')
    sel=int(aFile.read())
    a=glob.glob("./static/rooms/"+room+'/*.*')
    AfileName=a[sel][len('./static'):]
     
    return render_template('diapo.html', AfileName=AfileName)

@app.route('/display/<path:filename>')
def di(filename):
    return redirect(url_for('static', filename=filename), code=301)

@app.route('/diapo_admin', methods=['POST', 'GET'])
def diapo2():
    '''
    a=glob.glob("./static/rooms/"+room)
    if len(a)!=1:'''
    if not 'room'  in session:
        return redirect(url_for('diapo3'))
    else:
        upld=0
        slctd=0
        room=session['room']
        if request.method == 'POST':
            # check upload
            if 'file' in request.files:
                f_ile = request.files['file']
                if f_ile.filename !='':
                    filename = secure_filename(f_ile.filename)
                    f_ile.save(os.path.join("./static/rooms/"+room, filename))
                    upld=1
            # check if a file was selected
            if 'bt' in request.form:
                sel=request.form['bt']
                sel=int(sel.split('_')[0])
                path="./static/rooms/"+room+'/params/sel.txt'
                aFile=open(path,'w')
                aFile.write(str(sel)) 
                aFile.close()
                slctd=1 
                
                
        # get necessary dict
        
        d=glob.glob("./static/rooms/"+room+"/*.*")
        lenD=len(d)
        d_short=[elem.split('/')[-1] for elem in d]
        if slctd==0: sel=0
        messages=['',"<h1> File uploaded</h1>"][upld]+ ['',"<h1> File Selected</h1>"][slctd]
        return render_template('admin_diapo.html',d_short=d_short,d=d,lenD=lenD,sel=sel,msg=messages)
 
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file():
    return  render_template('download.html',value=filename)

@app.route('/serve-file/<path:filename>')
def return_files_tut(filename):
    file_path = './static/' + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

                     
@app.route('/diapo_admin_login', methods=['POST', 'GET'])
def diapo3():
    if request.method == 'POST':
        answer=request.form
        room=answer['room']
        pswd=answer['pswd']
        a=glob.glob("./static/rooms/"+room)
        if len(a)!=1:            
            #create room with password
            import os
            path="./static/rooms/"+room
            if not os.path.exists(path):
                  os.makedirs(path)
                  os.makedirs(path+'/params')
            aFile=open(path+'/params/pswd.txt','w')
            aFile.write(pswd)
            aFile.close()
            aFile=open(path+'/params/sel.txt','w')
            aFile.write('-1')
            aFile.close()
            session['room']=room
            session['pswd']=pswd
        else:
            a=glob.glob("./static/rooms/"+room+'/params/pswd.txt')
            aFile=open(a[0],'r')
            aFileContent=aFile.read()
            if aFileContent==pswd:
                session['room']=room
                session['pswd']=pswd
            else:
                return "Invalid Password"
            
        return redirect(url_for('diapo2')) 

    return '''Login or register in a room.<br>
<form method="post">
<label for="choice">Room</label>
<input name="room">
<label for="choice">Password</label>
<input name="pswd">
<input type="submit" name="b_selected"  value="Enter">'''
 
    
    

if __name__ == '__main__':
   #app.debug = True
   app.run()
   #app.run(debug = True)
