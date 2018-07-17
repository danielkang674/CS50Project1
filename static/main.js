document.body.onload = main;

function main(){
  let $loginBtn = document.getElementById("loginBtn");
  let $signupBtn = document.getElementById("signupBtn");
  let $container = document.getElementsByClassName("container");

  $loginBtn.onclick = function(){
    createLoginForm('login');
  };

  $signupBtn.onclick = function(){
    createLoginForm('signup');
  };

  let createLoginForm = function(action){
    let loginFormDiv;
    if(document.getElementById('loginFormDiv')){
      loginFormDiv = document.getElementById('loginFormDiv');
      while(loginFormDiv.lastChild){
        loginFormDiv.removeChild(loginFormDiv.lastChild);
      }
    } else{
      loginFormDiv = document.createElement("div");
      loginFormDiv.setAttribute('id', 'loginFormDiv');
    }
    let loginHeader = document.createElement('h2');
    loginHeader.textContent = action === 'login' ? 'Login to your account!' : 'Create a new account!';
    let loginForm = document.createElement('form');
    loginForm.setAttribute('method', 'post');
    loginForm.setAttribute('action', `/${action}`);
    loginForm.appendChild(createInputDiv(createInputField('text', 'userName', 'user name', 'form-control')));
    loginForm.appendChild(createInputDiv(createInputField('password', 'password', 'password', 'form-control')));
    if(action === 'signup') loginForm.appendChild(createInputDiv(createInputField('password', 'verifyPassword', 'verify password', 'form-control')));
    loginForm.appendChild(createInputDiv(createSubmitBtn()));
    loginFormDiv.appendChild(loginHeader);
    loginFormDiv.appendChild(loginForm);
    $container[0].appendChild(loginFormDiv);
  };

  let createInputField = function(type, name, placeholder, className){
    let tempInputNode = document.createElement('input');
    tempInputNode.className = className;
    tempInputNode.setAttribute('type', type);
    tempInputNode.setAttribute('name', name);
    tempInputNode.setAttribute('placeholder', placeholder);
    return tempInputNode;
  };

  let createInputDiv = function(node){
    let tempDivNode = document.createElement('div');
    tempDivNode.className = 'form-group';
    tempDivNode.appendChild(node);
    return tempDivNode;
  };

  let createSubmitBtn = function(){
    let tempButton = document.createElement('button');
    tempButton.setAttribute('type', 'submit');
    tempButton.className = 'btn btn-primary';
    tempButton.textContent += 'Submit';
    return tempButton;
  };
  
}