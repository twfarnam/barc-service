'use strict'
const webpack = require('webpack')
const notifier = require('node-notifier')
const path = require('path')
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')


module.exports = {

  entry: {
    app: './src/client/index.js'
  },

  resolve: {
    alias: { vue: 'vue/dist/vue.js' }
  },

  output: {
    filename: './static/app.js',
  },

  module: {

    rules: [

      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          cssSourceMap: true,
          cacheBusting: false,
        },
      },

      {
        test: /\.js$/,
        loader: 'babel-loader',
        include: [ './src', './node_modules/webpack-dev-server/client' ]
      },
  
    ]
  },

  devtool: 'cheap-module-eval-source-map',

  devServer: {
    clientLogLevel: 'warning',
    host: 'localhost',
    port: 5001,
    hot: true,
    open: false,
    overlay: { warnings: false, errors: true },
    quiet: true, // necessary for FriendlyErrorsPlugin
    watchOptions: { poll: false },
    proxy: { '/': 'http://127.0.0.1:5000' }
  },

  plugins: [
    // new webpack.DefinePlugin({ 'process.env': '"DEVELOPMENT"' }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NamedModulesPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
    new FriendlyErrorsPlugin({
      onErrors: (severity, errors) => {
        if (severity !== 'error') return

        const error = errors[0]
        const filename = error.file && error.file.split('!').pop()

        notifier.notify({
          title: 'Barc Webpack',
          message: severity + ': ' + error.name,
          subtitle: filename || '',
          icon: path.join(__dirname, 'static', 'icon.png')
        })
      } 
    })
  ],

}

