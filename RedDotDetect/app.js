var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var bodyParser = require('body-parser');
const port = process.env.PORT || 4000;

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var detectRouter = require('./routes/detect');

var redRouter = require('./routes/red');
var mqttRouter = require('./routes/mqtt');
var dtkRouter = require('./routes/dataToKotlin');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/detect', detectRouter);
app.use('/red', redRouter);
app.use('/mqtt', mqttRouter);
app.use('/dtk', dtkRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;

app.listen(port);
console.log('\nServer started at http://localhost:' + port );