const path = require('path');

module.exports = {
  entry: './static/assets/js/pdfview.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, './static/assets/js/')
  }
};