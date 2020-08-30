import axios from "axios"

export default axios.create({
    baseUrl: "http://127.0.0.1:5000",
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    },
    responseType: 'json',
    timeout: 1000 // ms
});
