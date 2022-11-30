from app import create_app

from app.models import Notification, Post, Reply, User 

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'User': User, 'Post': Post, 'Reply': Reply, 'Notification': Notification }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
