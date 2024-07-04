// models/event.js
const { Sequelize, DataTypes } = require('sequelize');

class Event extends Sequelize.Model {}
Event.init({
  title: {
    type: DataTypes.STRING
  },
  description: {
    type: DataTypes.STRING
  },
  date: {
    type: DataTypes.DATE
  },
  location: {
    type: DataTypes.STRING
  }
}, {
  sequelize,
  modelName: 'Event'
});

// models/user.js
const { Sequelize, DataTypes } = require('sequelize');

class User extends Sequelize.Model {}
User.init({
  name: {
    type: DataTypes.STRING
  },
  email: {
    type: DataTypes.STRING
  }
}, {
  sequelize,
  modelName: 'User'
});

// Example usage:
const event = new Event({
  title: 'Community Meeting',
  description: 'Monthly community meeting',
  date: new Date('2023-03-15'),
  location: 'City Hall'
});
event.save();

const user = new User({
  name: 'John Doe',
  email: 'johndoe@example.com'
});
user.save();