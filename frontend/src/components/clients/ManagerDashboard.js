import React, { Component, Fragment } from 'react';
//import axios from 'axios';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getClients, deleteClient } from '../../actions/clients';
//import ReactDOM, { render } from 'react-dom';
//axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
//axios.defaults.xsrfCookieName = "csrftoken";

export class Clients extends Component{

    static propTypes = {
        clients: PropTypes.array.isRequired,
        getClients: PropTypes.func.isRequired,
        deleteClient: PropTypes.func.isRequired
    };

    componentDidMount(){
        this.props.getClients();
    }

    render(){
        return(
            <Fragment>
                <h2>Clients</h2>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th />
                        </tr>
                    </thead>
                    <tbody>
                        { this.props.clients.map(client => (
                            <tr key={client.id}>
                                <td>{client.id}</td>
                                <td>{client.name}</td>
                                <td>
                                    <button onClick=
                                        {this.props.deleteClient.bind(this, client.id)} 
                                        className="btn btn-danger btn-sm">
                                        {" "}
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </Fragment>
        )
    }
}

const mapStateToProps = state => ({
    clients: state.clients.clients
});

export default connect(mapStateToProps, { getClients, deleteClient })(Clients);



//Working part, looks like all rendering will need to be held in a class
// that is an extension from component in order to not have {clients} 
// reinitialized or overriden to undefined

/*
const  managerDashboardService  =  new  ManagerDashboardService();

class  ClientsList  extends  Component {

constructor(props) {
    super(props);
    
    this.state  = {
        clients: [],

    }; 
}

componentDidMount() {
    var  self  =  this;
    managerDashboardService.getClients().then(function (results) {

        console.log(results);
        self.setState({ clients:  results})
    });
}

render() {


    return (
        <div  className="ManagerDashboard">
            <table  className="table">
            <thead  key="thead">
            <tr>
                <th>#</th>
                <th>name</th>
            </tr>
            </thead>
            <tbody>
            {this.state.clients.map( c  =>
                <tr  key={c.id}>
                <td>{c.id}  </td>
                <td>{c.name}</td>
                <td>
                </td>
            </tr>)}
            </tbody>
            </table>
        </div>
        );
  }
}
export  default  ClientsList;




*/




