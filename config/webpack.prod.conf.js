'use strict'
const path = require('path')
const webpack = require('webpack')
const merge = require('webpack-merge')
const baseWebpackConfig = require('./webpack.base.conf')
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')


module.exports = merge(baseWebpackConfig, {

  devtool: false,

  output: {
    path: '/',
    filename: 'static/[name].js',
  },

  plugins: [

    new webpack.DefinePlugin({ 'process.env': process.env.NODE_ENV }),

    new UglifyJsPlugin({
      uglifyOptions: { compress: { warnings: false } },
      sourceMap: false,
      parallel: true,
    }),

    new ExtractTextPlugin({
      filename: 'static/css/[name].css',
    }),

    // Compress extracted CSS. We are using this plugin so that possible
    // duplicated CSS from different components can be deduped.
    new OptimizeCSSPlugin({
      cssProcessorOptions: { safe: true, map: { inline: false } }
    }),

  ]
})



