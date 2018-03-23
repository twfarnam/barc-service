'use strict'
const path = require('path')
const webpack = require('webpack')
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')


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
          cssSourceMap: false,
          cacheBusting: false,
        },
      },

      {
        test: /\.js$/,
        loader: 'babel-loader',
        include: [ './src' ]
      },
  
    ]
  },

  devtool: false,

  plugins: [

    new webpack.DefinePlugin({ 'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }
    }),

    new UglifyJsPlugin({
      uglifyOptions: { compress: { warnings: false } },
      sourceMap: false,
      parallel: true,
    }),

    new OptimizeCSSPlugin({
      cssProcessorOptions: { safe: true, map: { inline: false } }
    }),

  ],

}



