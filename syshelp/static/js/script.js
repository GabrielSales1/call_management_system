const hamburguer = document.querySelector("#toggle-btn");

hamburguer.addEventListener("click",function(){
    document.querySelector("#sidebar").classList.toggle("expand");
})

$('#tabela').DataTable({
    language: {
        url: "https://cdn.datatables.net/plug-ins/1.13.7/i18n/pt-BR.json"
    }
});