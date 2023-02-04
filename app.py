from flask import Flask, jsonify, request
from flask_api import status
import requests
import itertools


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

post_url = "https://jsonplaceholder.typicode.com/posts"
comments_url = "https://jsonplaceholder.typicode.com/comments"


@app.route('/top_posts', methods=['GET'])
def top_post_by_comment():

    comments = requests.get(comments_url)

    if comments.status_code == 200:
        list_id = [key["postId"] for key in comments.json()]  # get list of post id

        post_id_occurences = {}
        for items in list_id:
            post_id_occurences[items] = list_id.count(items)  # count the occurence of each post id

         # sort comments based on post id (descending)
        sorted_comments = dict(sorted(post_id_occurences.items(), key=lambda x: x[1], reverse=True))
        top_comments = dict(itertools.islice(sorted_comments.items(), 0, 4))

        post = []

        for post_id, comments in enumerate(top_comments.items(), start=1):
            posts = requests.get(f'{post_url}/{post_id}')
            print(posts.json())
            postId = posts.json()['id']
            post_title = posts.json()['title']
            post_body = posts.json()['body']
            num_comments = comments[-1]

            post.append({
                'post_id': postId,
                'post_title': post_title,
                'post_body': post_body,
                'number_of_comments': num_comments
            })

    return post, status.HTTP_200_OK


@app.route('/comments', methods=['GET'])
def search_post():
    parameters = request.args.to_dict()

    if not parameters:
        return 'invalid request', 400

    post_id = parameters.get('postId', None),
    comment_id = parameters.get('id', None),
    name = parameters.get('name', None),
    email = parameters.get('email', None),

    post_id = post_id[0]
    comment_id = comment_id[0],
    name = name[0],
    email = email[0],

    if post_id is not None:
        filtered_comments = requests.get(f"{comments_url}?postId={int(post_id[0])}")

        return jsonify({
            'comment': filtered_comments.json()
        }), status.HTTP_200_OK


    if None not in (comment_id, name, email):
        filtered_comments = requests.get(f"{comments_url}?id={int(comment_id[0])}&name={name[0].strip()}&email={email[0].strip()}")

        return jsonify({
            'comments': filtered_comments.json()
        }), status.HTTP_200_OK
    
    else:
        return status.HTTP_400_BAD_REQUEST


if __name__ == '__main__':

    app.run(debug=True)
