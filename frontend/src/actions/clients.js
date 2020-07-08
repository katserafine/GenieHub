import axios from 'axios';

import { GET_CLIENTS, DELETE_CLIENT, ADD_CLIENT } from './types';

//GET CLIENTS LIST
export const getClients = () => dispatch => {
    axios.get('/api/clients')
    .then(res => {
        dispatch({
            type: GET_CLIENTS,
            payload: res.data
        });
    }).catch(err => console.log(err));
}

//DELETE A SINGLE CLIENT
export const deleteClient = (id) => dispatch => {
    axios.delete(`/api/clients/${id}`)
    .then(res => {
        dispatch({
            type: DELETE_CLIENT,
            payload: id
        });
    }).catch(err => console.log(err));
}

//ADD A SINGLE CLIENT
export const addClient = (client) => dispatch => {
    axios.post('/api/clients/', client)
    .then(res => {
        dispatch({
            type: ADD_CLIENT,
            payload: res.data
        });
    }).catch(err => console.log(err));
}

