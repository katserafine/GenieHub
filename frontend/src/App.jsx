import React from 'react';
import axios from 'axios';
import './App.css';



function handleClick(event) {

  axios
    .get(`api/Users/`).then((response) => { 
      //setResponseData(response.data)
      console.log(response.data)
    })
    .catch(err => console.log(err))
}


function App() {
  
  return (
    <div className="App">
      <div>
        <h3>hello there</h3>
      </div>
     <div>
        <button onClick={handleClick}>getUser</button>
      </div>
    </div>
  );

}

export default App;