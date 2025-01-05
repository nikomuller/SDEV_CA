const path = require("path");

module.exports = {
    entry: {
        carousel: './carousel/index.ts',
        login: './login/index.ts',
        register: './register/index.ts',
        store: './store/index.ts',
        reset: './reset/index.ts',
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                loader: 'ts-loader',
                exclude: /node_modules|\.d\.ts$/
            },
            {
                test: /\.d\.ts$/,
                loader: 'ignore-loader'
            },         
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }  
        ],
    },
    resolve: {
        extensions: [ '.ts', '.js' ],
    },
    output: {
        filename: '[name]_bin.js',
        path: path.resolve(__dirname, '../scillium/static/js'),
    },
};