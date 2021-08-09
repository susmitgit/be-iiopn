const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const DuplicatePackageCheckerPlugin = require('duplicate-package-checker-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
	mode: 'production',
	devtool: 'source-map',

	entry: [
		// 'bootstrap-loader',
		'webpack-hot-middleware/client',
		'./src/index'
	],
	output: {
		publicPath: 'dist/'
	},

	module: {
		rules: [
			{
				test: /\.(scss)$/,
				use: [
					{
						// inject CSS to page
						loader: 'style-loader'
					},
					{
						// translates CSS into CommonJS modules
						loader: 'css-loader'
					},
					{
						// Run postcss actions
						loader: 'postcss-loader',
						options: {
							// `postcssOptions` is needed for postcss 8.x;
							// if you use postcss 7.x skip the key
							postcssOptions: {
								// postcss plugins, can be exported to postcss.config.js
								plugins: function() {
									return [ require('autoprefixer') ];
								}
							}
						}
					},
					{
						// compiles Sass to CSS
						loader: 'sass-loader'
					}
				]
			}
		]
	},

	plugins: [
		new webpack.DefinePlugin({
			'process.env': {
				NODE_ENV: '"production"'
			},
			__DEVELOPMENT__: false
		}),
		new MiniCssExtractPlugin(),
		new DuplicatePackageCheckerPlugin(),
		new UglifyJsPlugin()
	]
};
