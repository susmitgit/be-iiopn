/* eslint camelcase: 0 */

import axios from 'axios';

const DEFAULT_HEADER = {
	'Content-Type': 'application/json'
};

const tokenConfig = (token) => ({
	headers: Object.assign({}, DEFAULT_HEADER, {
		Authorization: token // eslint-disable-line quote-props
	})
});

export function validate_token(token) {
	return axios.post('/api/v1/authorize', {
		token
	});
}

export function get_github_access() {
	window.open(
		'/github-login',
		'_blank' // <- This is what makes it open in a new window.
	);
}

export function create_user(username, email, password) {
	return axios.post(
		'/api/v1/users',
		{
			username,
			email,
			password
		},
		DEFAULT_HEADER
	);
}

export function get_token(email, password) {
	return axios.post(
		'/api/v1/authenticate',
		{
			email,
			password
		},
		DEFAULT_HEADER
	);
}

export function has_github_token(token) {
	return axios.get('/api/has_github_token', tokenConfig(token));
}

export function data_about_user(token) {
	return axios.get('/api/v1/me', tokenConfig(token));
}
