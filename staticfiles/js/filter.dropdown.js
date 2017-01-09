$('.filterElements').change(function(){
    document.getElementById('id_supervisor').getElementsByTagName('option')[0].selected = 'selected';
    var cl = document.getElementById('id_faculty').getElementsByTagName('option')[this.selectedIndex].getAttribute("class");
    console.log(cl)
    $('option').hide();
    $('option[class$="' + cl + '"]').show();
    $('option[id$="select"]').show();
});
