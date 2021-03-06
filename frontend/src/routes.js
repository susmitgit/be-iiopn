/* eslint new-cap: 0 */

import React from 'react';
import { Route, Switch, Redirect } from 'react-router';

/* containers */
import { App } from './containers/App';
import { HomeContainer } from './containers/HomeContainer';
import LoginView from './components/LoginView';
import RegisterView from './components/RegisterView';
import ProtectedView from './components/ProtectedView';
import Favourites from './components/Favourites';
import NotFound from './components/NotFound';

import { DetermineAuth } from './components/DetermineAuth';
import { requireAuthentication } from './components/AuthenticatedComponent';
import { requireNoAuthentication } from './components/notAuthenticatedComponent';

export default (
	<Switch>
		<Route path="/main" component={requireAuthentication(ProtectedView)} />
		<Route path="/login" component={requireNoAuthentication(LoginView)} />
		<Route path="/register" component={requireNoAuthentication(RegisterView)} />
		<Route path="/home" component={requireNoAuthentication(HomeContainer)} />
		<Route path="/Favourites" component={requireAuthentication(Favourites)} />
		<Route exact path="/">
			<Redirect to="/main" />
		</Route>
		{/* <Route path="*" component={DetermineAuth(NotFound)} /> */}
	</Switch>
);
