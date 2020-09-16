import gevent.monkey
gevent.monkey.patch_all()
import json
import flask
import socketio
import mysql.connector
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build as googleapiclient_build

conn = mysql.connector.connect(**json.load(open('secrets/mysql.json')))
conn.autocommit = True
cursor = conn.cursor()

web = flask.Flask(__name__)
web.secret_key = open('secrets/session.txt').read()
web.config['SERVER_NAME'] = 'project.easonkamander.com' # TODO
web.config['PREFERRED_URL_SCHEME'] = 'https'
skt = socketio.Server(async_mode='gevent_uwsgi')
app = socketio.WSGIApp(skt, web, socketio_path='/auth/ws/')

@web.route('/auth/') # Redirect To Google Auth
def auth():
	auth_send_flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
		client_secrets_file='secrets/oauth.json',
		redirect_uri=flask.url_for('auth_cb', _external=True),
		scopes=['openid']
	)
	auth_send_redirect_url, flask.session['nonce'] = auth_send_flow.authorization_url(access_type='offline', include_granted_scopes='true')
	return flask.redirect(auth_send_redirect_url)

@web.route('/auth/cb/') # Callback From Google Auth
def auth_cb():
	if 'nonce' in flask.session:
		auth_recv_flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
			client_secrets_file='secrets/oauth.json',
			redirect_uri=flask.url_for('auth_cb', _external=True),
			scopes=['openid'],
			state=flask.session['nonce']
		)
		flask.session.pop('nonce')
		auth_recv_flow.fetch_token(authorization_response=flask.request.url)
		crdt = google.oauth2.credentials.Credentials(
			token=auth_recv_flow.credentials.token,
			refresh_token=auth_recv_flow.credentials.refresh_token,
			token_uri=auth_recv_flow.credentials.token_uri,
			client_id=auth_recv_flow.credentials.client_id,
			client_secret=auth_recv_flow.credentials.client_secret,
			scopes=auth_recv_flow.credentials.scopes
		)
		service = googleapiclient_build('oauth2', 'v2', credentials=crdt)
		auth = service.userinfo().v2().me().get().execute()['id'] # pylint: disable=maybe-no-member
		cursor.execute('SELECT unid FROM users WHERE code = %(code)s', {'code': auth})
		result = cursor.fetchone()
		if result:
			flask.session['user'] = result[0]
		else:
			cursor.execute('INSERT INTO users (code) VALUES (%(code)s)', {'code': auth})
			flask.session['user'] = cursor.lastrowid
	return flask.redirect('/')

@web.route('/auth/rm/') # Clear Session
def auth_rm():
	flask.session.pop('user')
	return flask.redirect('/')

@skt.on('connect') # Connect To Websocket And Get Session Credentials
def skt_connect(sid, context):
	with web.request_context(context):
		skt.save_session(sid, {'user': flask.session['user'] if 'user' in flask.session else None})

@skt.on('custom_event') # Handle Websocket Events TODO
def skt_question(sid):
	print(skt.get_session(sid)['user'])