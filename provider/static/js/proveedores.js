/*here validate fiels**/
function validate_form()
{
        /*txtProvider
        txtRFC
        txtBanco
        txtSucursal
        txtCuenta
        txtClabe*/
        if ($('#txtProvider').val() == '')
        {
            msjAlert('El nombre del proveedor es necesario !');
        }
        else{
            if ($('#txtRFC').val() == '')
            {
                msjAlert('El RFC es nesesario !');
            }
            else{
                if ($('#txtBanco').val() == '')
                {
                     msjAlert('El banco es necesario !');
                }
                else{
                       if ($('#txtSucursal').val() == '')
                       {
                            msjAlert('La sucursal es necesaria !');
                       }
                      else{
                        if ($('#txtCuenta').val() == '')
                        {
                            msjAlert('La cuenta es necesaria !');
                        }
                       else{
                              if ($('#txtClabe').val() == '')
                              {
                                    msjAlert('La clave es necesaria !');
                              }
                              else{

                                    $.ajax({
                                            type:'POST',
                                            url: '/dashboard/provider/verify/',
                                            data:{
                                                    txtProvider:$("input[name=txtProvider]").val(),
                                                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                                                    },
                                            success:function(data)
                                            {
                                               if (data > 0)
                                               {
                                                    msjAlert(' El proveedor ya fue registrado por otra persona!');
                                               }
                                               else{
                                                        add_provider();
                                               }
                                            },
                                            error:function(req,e,er) {
                                                    msjError();
                                            }
                                            });
                              }
                       }
                      }
                }
            }
        }


}
/*save data of providers*/
function add_provider()
{
        $.ajax({
                type:'POST',
                url: '/dashboard/provider/add/',
                data:{
                        txtProvider:$("input[name=txtProvider]").val(),
                        txtRFC:$("input[name=txtRFC]").val(),
                        txtBanco:$("input[name=txtBanco").val(),
                        txtSucursal:$("input[name=txtSucursal").val(),
                        txtCuenta:$("input[name=txtCuenta").val(),
                        txtClabe:$("input[name=txtClabe").val(),
                        txtReferencia:$("input[name=txtReferencia").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                   if (data >= 1)
                   {
                       msjSucces('Proveedor registrado con exito !');
                       $("input[name=txtProvider]").val('');
                       $("input[name=txtRFC]").val('');
                       $("input[name=txtBanco").val('');
                       $("input[name=txtSucursal").val('');
                       $("input[name=txtCuenta").val('');
                       $("input[name=txtClabe").val('');
                       $("input[name=txtReferencia").val('');

                   }
                   else{
                          msjError();
                          $("input[name=txtProvider]").val('');
                          $("input[name=txtRFC]").val('');
                   }
                },
                error:function(req,e,er) {
                        msjError();
                }
                });

}
/*search provider*/
function search_provider()
{
        $("#tbSearch").empty();
        $("#DivContainer").show();
        $.ajax({
                type:'POST',
                url: '/dashboard/provider/search/',
                data:{
                        txtSearchProvider:$("input[name=txtSearchProvider]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                   $("#tbSearch").append(data);
                },
                error:function(req,e,er) {
                        msjError();
                }
                });
}

function setValuesEdit(Id,Provider,RFC,Banco,Sucursal,Cuenta,Clabe,Referencia)
{
    $("#txtEditId").val('');
    $("#txtProviderEdit").val('');
    $("#txtRFCEdit").val('');
    $("#txtBancoEdit").val('');
    $("#txtSucursalEdit").val('');
    $("#txtCuentaEdit").val('');
    $("#txtClabeEdit").val('');
    $("#txtReferenciaEdit").val('');

    $("#txtEditId").val(Id);
    $("#txtProviderEdit").val(Provider);
    $("#txtRFCEdit").val(RFC);
    $("#txtBancoEdit").val(Banco);
    $("#txtSucursalEdit").val(Sucursal);
    $("#txtCuentaEdit").val(Cuenta);
    $("#txtClabeEdit").val(Clabe);
    $("#txtReferenciaEdit").val(Referencia);

}

function save_edit()
{

    $.ajax({
            type:'POST',
            url: '/dashboard/provider/edit/',
            data:{
                    txtEditId:$("input[name=txtEditId]").val(),
                    txtProviderEdit:$("input[name=txtProviderEdit]").val(),
                    txtRFCEdit:$("input[name=txtRFCEdit]").val(),
                    txtBancoEdit:$("input[name=txtBancoEdit]").val(),
                    txtSucursalEdit:$("input[name=txtSucursalEdit]").val(),
                    txtCuentaEdit:$("input[name=txtCuentaEdit]").val(),
                    txtClabeEdit:$("input[name=txtClabeEdit]").val(),
                    txtReferenciaEdit:$("input[name=txtReferenciaEdit]").val(),
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                    },
            success:function(data)
            {
                   if (data >= 1)
                   {
                       msjSucces('Proveedor editado con exito !');
                       search_provider();
                   }
                   else{
                          msjError();
                   }
            },
            error:function(req,e,er) {
                    msjError();
            }
            });
}

function Cerrar_tap()
{
    $('#DivContainer').hide();
}

function verficar_proveedor(txtProveedor)
{
    $.ajax({
            type:'POST',
            url: '/dashboard/provider/verify/',
            data:{
                    txtProvider:$("input[name=txtProvider]").val(),
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                    },
            success:function(data)
            {
               return data;
            },
            error:function(req,e,er) {
                    msjError();
            }
            });
}