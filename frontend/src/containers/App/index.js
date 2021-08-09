import React from 'react';

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

/* application components */
import { Header } from '../../components/Header';
import { Footer } from '../../components/Footer';

/* global styles for app */
import './styles/app.scss';

export const App = (props) => {
	return (
		<MuiThemeProvider muiTheme={getMuiTheme()}>
			<section>
				<Header />
				<div className="container" style={{ marginTop: 20, paddingBottom: 250 }}>
					{props.children}
				</div>
				<div>
					<Footer />
				</div>
			</section>
		</MuiThemeProvider>
	);
};
