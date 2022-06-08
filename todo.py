from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__) #Flask class'ından bir nesne oluşturduk.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/user/Desktop/Proje_Ornekleri/To_Do_Application/todo.db' #Veritabanının yolunu belirledik.
db = SQLAlchemy(app) #SQLAlchemy sınıfından bir nesne oluşturduk.

class Todo(db.Model): #Todo sınıfımızı oluşturduk.@app.route'dan önce class olması gerekir.
    id = db.Column(db.Integer, primary_key=True) #id değişkenimizi oluşturduk.
    title = db.Column(db.String(80)) #title değişkenimizi oluşturduk.
    complete = db.Column(db.Boolean) #complete değişkenimizi oluşturduk.Boolean olmasının sebebi True ve False değerlerini tutmaktır.


@app.route("/")  #Ana sayfaya yönlendirme
def index():
    todos = Todo.query.all() #Todo sınıfımızın tüm verilerini alıyoruz.
    return render_template("index.html",todos=todos) #index.html dosyasının içinde todos değişkenimizi kullanacağımız için todos=todos şeklinde yazdık.
    
@app.route("/complete/<string:id>") #Todo'yu tamamlandı olarak işaretleme
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete #Todo'yu tamamlandı olarak işaretleme / Aşağıdaki IF döngüsü bu kod'un uzun hali.
    db.session.commit()
    return redirect(url_for("index"))
    #if todo.complete == True:
    #    todo.complete = False
    #else:
    #   todo.complete = True

@app.route("/delete/<string:id>") #Todo'yu silme
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add",methods=["POST"]) #POST methodu ile url map'ine bağlanıyoruz.
def addTodo():
    title = request.form.get("title") #Formdan gelen title değerini title değişkenine atadık.
    newTodo = Todo(title = title,complete = False) #Todo sınıfından bir nesne oluşturduk.
    db.session.add(newTodo) #Veritabanına ekleme yapıyoruz.
    db.session.commit() #Veritabanına yapılan değişiklikleri kaydediyoruz.
    return redirect(url_for("index")) #index.html sayfasına yönlendiriyoruz.
    
if __name__ == "__main__": #Eğer bu dosya direkt çalışırsa, aşağıdaki kodları çalıştır.
    db.create_all() #Veritabanımızı oluştur.app.run üstünde olmasının sebebi her seferinde class oluşturmaması için.
    app.run(debug=True) #debug=True parametresi ile hata ayıklama modunu açtık.
        