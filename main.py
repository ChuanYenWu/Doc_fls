from flask import Flask, render_template, request, send_file
from predict import image_gan
from PIL import Image
import io
import base64

app = Flask(__name__)

#@app.route("/")
#def home():
#    return render_template("home.html")
@app.route("/")
def index():
    hair_tag =['blonde hair', 'purple hair', 'red hair', 'blue hair', 'pink hair','green hair',
        'white hair', 'gray hair', 'black hair', 'brown hair', 'aqua hair', 'orange hair']
    eyes_tag =['pink eyes', 'purple eyes', 'aqua eyes', 'black eyes', 'blue eyes', 'yellow eyes',
        'green eyes', 'orange eyes', 'red eyes', 'brown eyes', 'gray eyes']
    context = {
        'hair_tag' : hair_tag,
        'eyes_tag' : eyes_tag,
    }
    return render_template("index.html", **context)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/predict',methods=['POST'])
def predict():
    
    if request.method == 'POST':
        hair_color = request.form["hair_color"]
        eyes_color = request.form["eyes_color"]

        f_image = image_gan( hair_color, eyes_color)
        f_image = Image.fromarray(f_image)
        file_object = io.BytesIO()
        f_image.save(file_object, 'PNG')
        file_object.seek(0)

        encoded_img_data = base64.b64encode(file_object.getvalue())
        #base64_encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    

    #return send_file(file_object, mimetype='image/PNG')
    return render_template("result.html", img_data=encoded_img_data.decode('utf-8'))
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
#render_template將會找尋html檔案傳送給使用者