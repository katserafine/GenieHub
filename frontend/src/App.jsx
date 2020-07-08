import React, { Component } from 'react';
//import axios from 'axios';
//import { BrowserRouter as Router, Route} from 'react-router-dom';
//import  ClientsList from './clients/ManagerDashboard'
//import  ClientCreateUpdate  from './clients/ManagerDashboardModify'
import './App.css';
//import HomePage from './cores/homePage';
import Header from './components/layout/Header';
import Dashboard from './components/clients/Dashboard';
import { Provider } from 'react-redux';
import store from './store';


class App extends Component {
  render(){
    return (
      <Provider store={store}>
        <React.Fragment> 
          <Header />
          <div className="container">
            <Dashboard />
          </div>
        </React.Fragment>
    </Provider>
    )
  }
}

// in reality the following will need to be put into clients folder in a new file that 
//  is called when manager wants to view
/*
const BaseLayout = () => (

  <React.Fragment>
  
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"></link>
  
  
  <div className="container-fluid">
    <nav  className="navbar navbar-expand-lg navbar-light bg-light">
        <a  className="App" hef="id">Geniehub</a>
        <button  className="navbar-toggler"  type="button"  data-toggle="collapse"  data-target="#navbarNavAltMarkup"  aria-controls="navbarNavAltMarkup"  aria-expanded="false"  aria-label="Toggle navigation">
        <span  className="navbar-toggler-icon"></span>
    </button>
    <div  className="collapse navbar-collapse"  id="navbarNavAltMarkup">
        <div  className="navbar-nav">
            <a  className="nav-item nav-link"  href="/">View all Clients  </a>
            <a  className="nav-item nav-link"  href="/client">  Add a Client</a>
        </div>
    </div>
    </nav>

    <div className="content">
      <Route path="/" exact component={ClientsList} />
      <Route path="/client/:pk"  component={ClientCreateUpdate} />
      <Route path="/client/" exact component={ClientCreateUpdate} />

    </div>

  </div>
  
  </React.Fragment>
)

class App extends Component {
  render() {
    return (
      <Router>
        <BaseLayout/>
      </Router>
    );
  }
}
*/
////////////////////////////////////////////////////////////////////////////////////
/*

//import React, { Component } from 'react';
import Nav from './cores/Nav';
import LoginForm from './cores/LoginForm';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayed_form: '',
      logged_in: localStorage.getItem('token') ? true : false,
      username: ''
    };
  }

  componentDidMount() {
    var self = this;
    if (this.state.logged_in) {
      axios.get('/core/current_user/', {
        headers: {
          Authorization: `JWT ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(json => {
          this.setState({ username: json.username });
        });
    }
  }

  handle_login = (e, entered) => {
    var self = this;
    e.preventDefault();
    axios.request('token-auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      data: {
        username: entered.username,
        password: entered.password
      }
    })
      //.then(res => res.json())
      .then(res => res.data).then(data => {
        console.log(data.token);
        localStorage.setItem('token', data.token);
        self.setState({
          logged_in: true,
          displayed_form: '',
          username: data.user.username
        });
      });
  };


  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({ logged_in: false, username: '' });
  };

  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  render() {
    let form;
    switch (this.state.displayed_form) {
      case 'login':
        form = <LoginForm handle_login={this.handle_login} />;
        break;
      default:
        form = null;
    }

    return (
      <div className="App">
        <Nav
          logged_in={this.state.logged_in}
          display_form={this.display_form}
          handle_logout={this.handle_logout}
        />
        {form}
        <h3>
          {this.state.logged_in
            ? `Hello, ${this.state.username}`
            : 'Please Log In'}
        </h3>
      </div>
    );
  }
}







*/












///////////////////////////////////////////////////////////////////////////////////////

/*
//possible starting setup

const BaseLayout = () => (

  <React.Fragment>
  
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"></link>
  
  
  <div className="container-fluid">
    <nav  className="navbar navbar-expand-lg navbar-light bg-light">
        <a  className="navbar-brand" hef="/">Geniehub</a>
        <button  className="navbar-toggler"  type="button"  data-toggle="collapse"  data-target="#navbarNavAltMarkup"  aria-controls="navbarNavAltMarkup"  aria-expanded="false"  aria-label="Toggle navigation">
        <span  className="navbar-toggler-icon"></span>
    </button>
    <div  className="collapse navbar-collapse"  id="navbarNavAltMarkup">
    <div  className="navbar-nav">
            <a  className="nav-item nav-link"  href="/login">Login or Logout </a>
        </div>
    </div>
    </nav>

    <div className="content">
      <Route path="/login" exact component={HomePage} />
      <Route path="/dashboard" eact component={ClientsList} />
     </div>

  </div>
  
  </React.Fragment>

)


class App extends Component {
  render() {
    return (
      <Router>
        <BaseLayout/>
      </Router>
    );
  }
}

*/

export default App;


