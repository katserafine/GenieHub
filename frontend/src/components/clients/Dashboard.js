import React from 'react';
import Form from './Form';
import Clients from './ManagerDashboard'

export default function Dashboard() {
    return(
        <React.Fragment>
            <Form />
            <Clients />
        </React.Fragment>
    )
}