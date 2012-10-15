//functie de lightbox in cazul in care da click pe background sa dispara dar nu si cand da click pe vrun copil
function remove_lightbox(){
    $('.lightbox').click(function(){
        $(this).parent().remove();
        location.reload();
        return false;
    });
}
