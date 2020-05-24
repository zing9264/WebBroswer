
const csrf_token = document.querySelector('#csrfmiddlewaretoken');

fetch('http://127.0.0.1:8000/getcsrf/', {})
  .then((response) => {
    console.log(response);
    return response.json(); 
  }).then((data) => {
      console.log(data);
      csrf_token.value =data['csrf_token'];
  }).catch((err) => {
    console.log('錯誤:', err);
});
