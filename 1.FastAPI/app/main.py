from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time





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





@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts=cursor.fetchall()
    print(posts)
    return {"message":posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute(""" INSERT INTO posts (title, content ,published) VALUES (%s, %s, %s) RETURNING* """,(post.title, post.content, post.published))
    post = cursor.fetchone()

    conn.commit()


    return {"data":post}


@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    post= cursor.fetchone()

    if not post:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found"))
    
    print(post)
    return {"post_detail":post} 
 


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    
    cursor.execute("""DELETE FROM posts WHERE id=%s returning*""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if  delete_post == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found"))
        response.status_code= status.HTTP_404_NOT_FOUND
    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    
    cursor.execute("""UPDATE posts  SET title =%s, content= %s, published=%s WHERE id=%s RETURNING * """,(post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    

    if update_post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id:{id} was not found")
    

    return {"data": update_post}
    

'''

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    
    post_query.update({'title':'hey this is my updated title','content':'hey this ismy updated content'},synchronize_session=False)
    
    
    return {"data":post}

'''

             
     
    
    
   
      
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