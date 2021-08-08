import React, { Component } from 'react';
import { useHistory } from 'react-router';
import { useDispatch, useSelector } from 'react-redux';
import { bindActionCreators } from 'redux';
import AppBar from 'material-ui/AppBar';
import LeftNav from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import FlatButton from 'material-ui/FlatButton';
import Divider from 'material-ui/Divider';

import * as authActions from '../../actions/auth';
import * as optionActions from '../../actions/option';

function mapStateToProps(state) {
	return {
		token: state.auth.token,
		userName: state.auth.userName,
		isAuthenticated: state.auth.isAuthenticated
	};
}

export const Header = () => {
	const history = useHistory();
	const dispatch = useDispatch();
	const sideBarOpen = useSelector((state) => state.option.sideBarOpen);
	const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

	const dispatchNewRoute = (route) => {
		dispatch(optionActions.setSideBarOpen(false));
		history.push(route);
	};

	const handleClickOutside = () => {
		dispatch(optionActions.setSideBarOpen(false));
	};

	const logout = (e) => {
		e.preventDefault();
		dispatch(authActions.logoutAndRedirect(history));
		dispatch(optionActions.setSideBarOpen(false));
	};

	const openNav = () => {
		dispatch(optionActions.setSideBarOpen(true));
	};

	return (
		<header>
			<LeftNav open={sideBarOpen}>
				{!isAuthenticated ? (
					<div>
						<MenuItem onClick={() => dispatchNewRoute('/login')}>Exisiting user</MenuItem>
						<MenuItem onClick={() => dispatchNewRoute('/register')}>New register</MenuItem>
					</div>
				) : (
					<div>
						<MenuItem onClick={() => dispatchNewRoute('/Favourites')}>My Favourites</MenuItem>
						<Divider />

						<MenuItem onClick={(e) => logout(e)}>Logout</MenuItem>
					</div>
				)}
			</LeftNav>
			<AppBar
				title="IIOPEN: Is it open?"
				onLeftIconButtonClick={() => openNav()}
				iconElementRight={<FlatButton label="Main" onClick={() => dispatchNewRoute('/')} />}
			/>
		</header>
	);
};
