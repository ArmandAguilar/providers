function login()
{
    if($("#txtUsuario").val() == '')
     {
            $("#fieldUsuario").addClass("has-feedback has-error");
     }
    else
        {
            $("#fieldUsuario").removeClass("has-feedback has-error");
            if($("#txtPassword").val() == '')
            {
                $("#fieldPassword").addClass("has-feedback has-error");
            }
            else{
                  $("#fieldPassword").removeClass("has-feedback has-error");
                  $.ajax({
                        type:'POST',
                        url: '/login/make_login/',
                        data:{
                                Nick:$("input[name=txtUsuario]").val(),
                                Password:$("input[name=txtPassword]").val(),
                                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                                },
                        success:function(data)
                        {
                            if (data > 0)
                                window.location.href  = '/pagos/'
                            else
                                 alert('Error en el password');
                        },
                        error:function(req,e,er) {

                        }
                        });
                }
        }
}
