from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
   
   

app = FastAPI()






class Post(BaseModel):
    title: str
    content:str
    published:bool =True
while True:
    try:
        conn= psycopg2.connect(host='localhost' ,database='fastapi' ,user='postgres' ,password='admin')
        conn.cursor_factory=RealDictCursor 
        cursor= conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error: ",error )
        time.sleep(2)

my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},{"title":"tiele of post 2","content":"content of post 2","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i


@app.get("/")
def root():
    return {"message":"welcome to my api"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts= db.query(models.Post).all()
    

    return {"data" : posts}





@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts """)
    #posts=cursor.fetchall()
    posts= db.query(models.Post).all()
    return {"message":posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db: Session = Depends(get_db)):
    #cursor.execute(""" INSERT INTO posts (title, content ,published) VALUES (%s, %s, %s) RETURNING* """,(post.title, post.content, post.published))
    #new_post=cursor.fetchone()

    #conn.commit()


    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data":new_post}


@app.get("/posts/{id}")
def get_post(id:int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    #test_post= cursor.fetchone()

    post= db.query(models.Post).filter(models.Post.id ==id).first()
    print(post)

    if not post:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found"))
    
    print(post)
    return {"post_detail":post} 
 
 



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    
    #cursor.execute("""DELETE FROM posts WHERE id=%s returning*""",(str(id),))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    
    post=db.query(models.Post).filter(models.Post.id == id)
   
    
    if  post.delete == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found"))
        #response.status_code= status.HTTP_404_NOT_FOUND
    
    post.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post,  db: Session = Depends(get_db)):
    
    #cursor.execute("""UPDATE posts  SET title =%s, content= %s, published=%s WHERE id=%s RETURNING* """,(post.title,post.content,post.published,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id == id)

    post=post_query.first()
    
    



    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    
    post_query.update(post.dict(), synchronize_session=False)
    
    
    return {"data":post}



             
     
    
    
   
      
'''#index=find_index_post(id)
    #if not index:
    #    raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found"))
    #    #response.status_code= status.HTTP_404_NOT_FOUND
    #my_posts.pop(index)'''



'''@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    post_dict=post.dict()

    post_dict['id']= randrange(1,1000000)
    my_posts.append(post_dict)
    return {"data":my_posts}'''