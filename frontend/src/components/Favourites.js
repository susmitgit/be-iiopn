import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as actionCreators from '../actions/auth';

function mapStateToProps(state) {
	return {
		isRegistering: state.auth.isRegistering,
		registerStatusText: state.auth.registerStatusText
	};
}

function mapDispatchToProps(dispatch) {
	return bindActionCreators(actionCreators, dispatch);
}

@connect(mapStateToProps, mapDispatchToProps)
class Favourites extends React.Component {
	// eslint-disable-line react/prefer-stateless-function
	render() {
		return (
			<div className="col-md-8">
				<h1>My Favourites</h1>
				<hr />
			</div>
		);
	}
}

export default Favourites;
