from flask import Flask,render_template,request
import pickle 
import numpy as np

popular_df=pickle.load(open('popular.pkl','rb'))
pt =pickle.load(open('pt.pkl','rb'))
books =pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))

#makig simple web app or website
app= Flask(__name__)


@app.route("/",methods=["GET"])
def welcome():
    return render_template('index.html',
                            book_name=list(popular_df['Book-Title'].values),
                            author=list(popular_df['Book-Author'].values),
                            image=list(popular_df['Image-URL-M'].values),
                            votes=list(popular_df['num_ratings'].values),
                            ratings=list(popular_df['avg_rating'].values)
                            )

@app.route("/recommand")
def recommand_ui():
   return render_template('recommand.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index =np.where(pt.index==user_input)[0][0]
    similer_item=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data=[]
    for i in similer_item:
        item=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
        print(data)
    
    return render_template('recommand.html',data=data)

