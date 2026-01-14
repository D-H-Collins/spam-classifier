from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import keras
import re
import numpy as np

model = keras.saving.load_model('spamclass.keras')
pattern_unusual = r'[^\w\sa!@#$%^&£*()_+\-=\[\]{};\':"\\|,.<>\/?]' #Pattern which selects characters not inside brackets.

threshold = 0.85 #Adjustable Threshold for classifier


#Function to format the string and run the model. Model handles vectorization including unknown tokens.
def eval(x: str):
    x = x.replace('\u2018', '\'')
    x = re.sub(pattern_unusual, '', x)
    x = np.array(x).reshape(1,1)
    return int(model(x,training=False)>threshold)


x = eval('abc')
print(x)
app = FastAPI()

#Verification message.
@app.get('/')
async def root():
    return{'message': 'verification'}

#Spam checker
@app.get('/spamcheck')
async def spam_check(text: str):
    if len(text) > 160: #Max SMS Sized
        raise HTTPException(status_code=422, detail='Input string too long.')
    return(eval(text))    


