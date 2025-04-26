from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

next_id = 3


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction')

    sorted_posts = POSTS.copy()

    if sort_field:
        if sort_field not in ['title', 'content']:
            return jsonify({'error': 'Invalid sort field. Must be "title" or "content".'}), 400

        reverse = False
        if direction:
            if direction == 'desc':
                reverse = True
            elif direction != 'asc':
                return jsonify({'error': 'Invalid direction. Must be "asc" or "desc".'}), 400

        sorted_posts.sort(key=lambda post: post.get(sort_field, '').lower(), reverse=reverse)

    return jsonify(sorted_posts), 200



@app.route('/api/posts', methods=['POST'])
def add_post():
    global next_id
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Both title and content are required.'}), 400

    new_post = {
        'id': next_id,
        'title': data['title'],
        'content': data['content']
    }

    POSTS.append(new_post)
    next_id += 1

    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_to_delete = None
    for post in POSTS:
        if post['id'] == post_id:
            post_to_delete = post
            break

    if post_to_delete is None:
        return jsonify({'error': f'Post with id {post_id} not found.'}), 404

    POSTS.remove(post_to_delete)
    return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    post_to_update = None
    for post in POSTS:
        if post['id'] == post_id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({'error': f'Post with id {post_id} not found.'}), 404

    if 'title' in data:
        post_to_update['title'] = data['title']
    if 'content' in data:
        post_to_update['content'] = data['content']

    return jsonify(post_to_update), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    # Filter posts based on title and/or content search terms
    results = []

    for post in POSTS:
        matches_title = title_query.lower() in post['title'].lower() if title_query else False
        matches_content = content_query.lower() in post['content'].lower() if content_query else False

        if matches_title or matches_content:
            results.append(post)

    return jsonify(results), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

