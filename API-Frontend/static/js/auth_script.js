// Alternar entre login e cadastro
const formLogin = document.getElementById("formLogin");
const formCadastro = document.getElementById("formCadastro");
const linkCadastro = document.getElementById("linkCadastro");
const linkLogin = document.getElementById("linkLogin");

linkCadastro.addEventListener("click", (e) => {
  e.preventDefault();
  formLogin.classList.remove("active");
  formCadastro.classList.add("active");
});

linkLogin.addEventListener("click", (e) => {
  e.preventDefault();
  formCadastro.classList.remove("active");
  formLogin.classList.add("active");
});

// Validação de cadastro (apenas frontend)
formCadastro.addEventListener("submit", (e) => {
  const senha = document.getElementById("senha").value;
  const confirmarSenha = document.getElementById("confirmarSenha").value;
  const msg = document.getElementById("cadastroMsg");

  if (senha !== confirmarSenha) {
    e.preventDefault();
    msg.textContent = "As senhas não coincidem!";
    msg.style.color = "red";
    return false;
  }
  
  // Se as senhas coincidirem, o formulário será enviado normalmente
  return true;
});
