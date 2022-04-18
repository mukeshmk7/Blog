from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)

with open('url.txt') as f:
    url = f.readlines()
 
url_link = url[0].split("=", maxsplit=1)[1].strip()
post_objects = []
blog_url = requests.get(url=url_link)
blog_url.raise_for_status()
blogs = blog_url.json()
for blog in blogs:
    post_obj = Post(blog["id"], blog["title"], blog["subtitle"], blog["body"])
    post_objects.append(post_obj)


@app.route('/')
def home():
    return render_template("index.html", blogs=post_objects)


@app.route('/post/<int:num>')
def blog_fn(num):
    req_post = None
    for obj in post_objects:
        if obj.id == num:
            req_post = obj
    return render_template("post.html", post=req_post)


if __name__ == "__main__":
    app.run(debug=True)
