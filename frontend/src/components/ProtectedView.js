import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useComponentDidMount, useComponentDidUpdate } from '../utils/lifecycle_hook';
import * as dataActions from '../actions/data';

const ProtectedView = (props) => {
	const data = useSelector((state) => state.data);
	const token = useSelector((state) => state.auth.token);
	const loaded = data.loaded;
	const email = data.data ? data.data.email : '';
	const username = data.data ? data.data.username : '';
	const dispatch = useDispatch();

	useComponentDidMount(() => {
		dispatch(() => dataActions.fetchProtectedData(token, dispatch));
	});

	return (
		<div>
			{!loaded ? (
				<h1>Loading data...</h1>
			) : (
				<React.Fragment>
					<div>
						<div style={{ float: 'left' }}>
							<h1 style={{ textAlign: 'left', fontSize: 'large' }}>Welcome back, {username}!</h1>
						</div>
						<div style={{ float: 'right' }}>
							<h1 style={{ textAlign: 'right', fontSize: 'large' }}>{email}</h1>
						</div>
					</div>
					<div>{/* Body  */}</div>
				</React.Fragment>
			)}
		</div>
	);
};

export default ProtectedView;

// ProtectedView.propTypes = {
//     fetchProtectedData: React.PropTypes.func,
//     loaded: React.PropTypes.bool,
//     userName: React.PropTypes.string,
//     data: React.PropTypes.any,
//     token: React.PropTypes.string,
// };
