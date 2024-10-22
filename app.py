from  flask import Flask,redirect,render_template,request,send_file
from fpdf import FPDF
import pandas as pd
import joblib
from fpdf import FPDF
import pandas as pd
import numpy as np

def create_pdf(name,a,g,h,w,bmi,p,d,s,st,pa,ch,all,alc,tob,blo,glu,hea,tem,bloodtest,rs):
  
    data = {
        'Name':[name],
        'Age': [a],
        'Gender': [g],
        'Height (cm)': [h],
        'Weight (kg)': [w],
        'BMI': [bmi],
        'Physical Activity Level': [p],
        'Dietary Habits': [d],
        'Sleep Patterns': [s],
        'Stress Level': [st],
        'Past Surgeries': [pa],
        'Chronic Conditions': [ch],
        'Allergies': [all],
        'Alcohol Consumption': [alc],
        'Tobacco Use': [tob],
        'Blood Pressure (mmHg)': [blo],
        'Glucose (mg/dL)': [glu],
        'Heart Rate (bpm)': [hea],
        'Temperature (°C)': [tem],
        'Blood Test Parameters': [bloodtest],
        'Risk Score': [rs]
    }

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Step 1: Create a PDF and add the watermark image at the top
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add the transparent logo as a watermark at the top
    pdf.image('static/img.jpg', x=1, y=1, w=70, h=31)  # Adjust 'x', 'y', 'w', 'h' as needed

    # Title of the PDF centered
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Patient Medical Report", ln=True, align='C')  # Width 0 ensures the cell takes the entire page width
    pdf.ln(10)  # Line break static\img.jpg

    # Add the data to the PDF in a tabular format with left padding
    pdf.set_font("Arial", size=12)
    for col, value in df.iloc[0].items():
        pdf.set_x(15)  # Set left padding of 15px
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(80, 10, f"{col}:", border=1)
        pdf.set_font("Arial", size=12)
        pdf.cell(100, 10, f"{value}", border=1, ln=True)

    # Save PDF
    pdf_output = "Result.pdf"
    pdf.output(pdf_output)
    

    #print(f"PDF created: {pdf_output}")




app = Flask(__name__)



model = joblib.load('NxtGenHealth')
@app.route('/download_pdf')
def download_pdf():
    pdf_path = 'Result.pdf'
    return send_file(pdf_path, as_attachment=True, download_name="Result.pdf")
  
  
@app.route('/',methods=['POST','GET'])
def index():
  if request.method=='POST':
    first = request.form['first']
    last = request.form['last']        
    age = request.form['age']
    gen = request.form['gen']
    hei = request.form['height']
    wei = request.form['weight']
    phyact=request.form['phyact']
    diet = request.form['diet']
    sleep = request.form['sleep']
    stress= request.form['stress']
    smoking = request.form['smoking']
    Alcon = request.form['Alcon']
    PastSur = request.form['PastSur']
    chronic = request.form['chronic']
    glucose = request.form['glucose']
    heart_rate = request.form['heart-rate']
    allergy = request.form['allergy']
    temp = request.form['temp']
    Bp = request.form['Bp']
    bloodtest = request.form['bloodtest']
    #da = request.form['da']
    #print([first,last,age,gen,hei,wei,phyact,diet,sleep,stress,smoking,Alcon,PastSur,chronic,glucose,heart_rate,allergy,temp,Bp])
    
    age = int(age)
    if gen == 'Male':
      gen =1
    elif gen == 'Female':
      gen =0
    else:
      gen =1
    hei = int(hei)
    wei = int(wei)
    if phyact == 'Low':
      phyact = 0
    elif phyact == 'Moderate':
      phyact = 1
    else:
      phyact =2
    if diet == 'Veg':
      diet = 0
    elif diet == 'Balanced Diet':
      diet = 1
    else:
      diet = 2
    sleep = int(sleep)
    if stress == 'Low (4 hrs)':
      stress = 0
    elif stress == 'Moderate (6-8 hrs)':
      stress= 1
    else:
      stress = 2
    if smoking == 'No':
      smoking=0
    else:
      smoking=1
    if Alcon == 'No':
      Alcon =0
    elif Alcon == 'Occasionally':
      Alcon = 1
    else:
      Alcon = 2
    if PastSur == 'Yes':
      PastSur = 1
    else:
      PastSur = 0
    if chronic == 'No':
      chronic = 0
    elif chronic == 'Diabetes':
      chronic = 1
    elif chronic == 'Hypertension':
      chronic = 2
    elif chronic == 'Asthma':
      
      chronic = 3
    glucose = int(glucose)
    heart_rate = int(heart_rate)
    if allergy == 'No':
      allergy = 0
    elif allergy == 'Food Allergies':
      allergy = 1
    elif allergy == 'Pollen Allergies':
      allergy = 2
    elif allergy == 'Pencillin Allergies':
      allergy = 3
    temp = float(temp)
    Bp = Bp.split('/')
    Bpmm = Bp[0]
    Bpmm = int(Bpmm)
    Bphg = Bp[1]
    Bphg = int(Bphg)
    #print([first,last,age,gen,hei,wei,phyact,diet,sleep,stress,smoking,Alcon,PastSur,chronic,glucose,heart_rate,allergy,temp,Bpmm,Bphg])
    
    bmi = wei / ((hei*0.01)*(hei*0.01))
    prediction = model.predict(pd.DataFrame({'Age':age,'Gender':gen,'Height (cm)':hei,'Weight (kg)':wei,'BMI':bmi,'Physical Activity Level':phyact,'Dietary Habits':diet,'Sleep Patterns':sleep,'Stress Level':stress,'Past Surgeries':PastSur,'Chronic Conditions':chronic,'Allergies':allergy,'Alcohol Consumption':Alcon,'Tobacco Use':smoking,'Glucose (mg/dL)':glucose,'Heart Rate (bpm)':heart_rate,'Temperature (°C)':temp,'Blood Pressure (mm)':Bpmm,'Blood Pressure (Hg)':Bphg},index=[0]))
    if gen == 1:
      gen = "Male"
    else:
      gen = "Female"
    if phyact == 0:
      phyact = 'Low'
    elif phyact == 1:
      phyact = 'Moderate'
    else:
      phyact = 'High'
    if diet == 0:
      diet = "Veg"
    elif diet == 1:
      diet = "Balanced Diet"
    else:
      diet = "Non Veg"
    if stress == 0:
      stress = 'Low (4 hrs)'
    elif stress == 1:
      stress = 'Moderate (6-8 hrs)'
    else:
      stress = 'High(>8 hrs)'
    if PastSur == 0:
      PastSur = 'No'
    else:
      PastSur = 'Yes'
    if chronic == 0:
      chronic ='No'
    elif chronic == 1:
      chronic = 'Diabetes'
    elif chronic == 2:
      chronic = 'Hypertension'
    else:
      chronic = 'Asthma'
    
    if allergy == 0:
      allergy = 'No'
    elif allergy == 1:
      allergy = 'Food Allergies'
    elif allergy == 2:
      allergy = 'Pollen Allergies'
    else:
      allergy = 'Pencillin Allergies'
    
    if Alcon == 0:
      Alcon = 'No'
    elif Alcon == 1:
      Alcon = 'Occasionally'
    else:
      Alcon = 'Regularly'
    
    
    if smoking == 0:
      smoking = 'No'
    else:
      smoking = 'Yes'
    name = first + ' ' + last
    arr = np.array([prediction], dtype=np.float32)

    rounded_value = np.around(arr, 2)

    create_pdf(name,age,gen,hei,wei,bmi,phyact,diet,sleep,stress,PastSur,chronic,allergy,Alcon,smoking,Bp,glucose,heart_rate,temp,bloodtest,rounded_value)
    
    if rounded_value >=0 and rounded_value <0.5:
      return render_template('No risk.html',name=name,age=age,gen=gen)
    elif rounded_value == 0.5:
      return render_template('Low Risk.html',name=name,age=age,gen=gen)
    else:
      return render_template('high risk.html',name=name,age=age,gen=gen)
      
      
      
    
      

    
    
    
  return render_template('NxtGenHealth.html')
  
  
  


@app.route('/final')

def final():
  return render_template('high risk.html')
  
  
  
  
if __name__ == "__main__":
  app.run(debug=True)