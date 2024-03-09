import flask
from flask import jsonify, make_response, app, request

from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print(jobs)
    return jsonify(
        {
            'jobs':
                [item.to_dict(
                    only=('job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'is_finished', 'user.name'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        @app.errorhandler(404)
        def not_found(error):
            return make_response(jsonify({'error': 'Not found'}), 404)

        @app.errorhandler(400)
        def bad_request(_):
            return make_response(jsonify({'error': 'Bad Request'}), 400)

    return jsonify(
        {
            'jobs': jobs.to_dict(
                only=('job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'is_finished', 'user.name'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})
