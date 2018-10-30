function search_provider()
{

    $("#tbSearch").empty();
    $('#DivContainerSearch').hide();
        $("#DivContainer").show();
        $.ajax({
                type:'POST',
                url: '/contrato/search/provider/',
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
/*here set idprovider */
function set_Provider(id,name)
{
    $("#txtIdProveedor").val();
    $("#txtIdProveedor").val(id);
    $("#lblProvider").empty();
    $("#lblProvider").append(name);
    $("#DivContainer").hide();
}
/*here save the data*/
function save_data()
{

    if($("#txtContrato").val() == '')
    {
        msjAlert('El campo Contrato no puede estar vacio.');
    }
    else{
            if($("#txtIdProveedor").val() == '')
            {
                msjAlert('Debes selecionar un proveedor.');
            }
            else{
                    if($("#txtxMonto").val() == '')
                      {
                         msjAlert('El monto no puede estra vacio.');
                      }
                     else{
                            $.ajax({
                            type:'POST',
                            url: '/contrato/verify/',
                            data:{
                                    txtContrato:$("input[name=txtContrato]").val(),
                                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                                    },
                            success:function(data)
                            {
                                   if (data > 0)
                                   {
                                       //Alerta
                                        msjAlert(' El contrato ya existe')
                                   }
                                   else{
                                          send_data();
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

function send_data()
{
    $.ajax({
            type:'POST',
            url: '/contrato/save/',
            data:{
                    txtContrato:$("input[name=txtContrato]").val(),
                    txtIdProveedor:$("input[name=txtIdProveedor]").val(),
                    txtMonto:$("input[name=txtMonto]").val(),
                    txtIVA:$("input[name=txtIVA]").val(),
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    },
            success:function(data)
            {

                   if (data >= 1)
                   {
                       msjSucces('Contrato asigando con exito !');
                       $('#txtSearchProvider').val('');
                       $('#txtContrato').val('');
                       $("#txtMonto").val('');
                       $("#txtIVA").val('');
                       $('#lblProvider').empty();
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
/*here search contract*/
function search_contract()
{
    $('#tbSearchContratos').empty();
    $('#DivContainer').hide();
    $('#DivContainerSearch').show();
    $.ajax({
            type:'POST',
            url: '/contrato/search/contrato/',
            data:{
                    txtSearchContrato:$("input[name=txtSearchContrato]").val(),
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    },
            success:function(data)
            {
                $('#tbSearchContratos').append(data);
            },
            error:function(req,e,er) {
                    msjError();
            }
            });
}
/*here edit contract */
function setEdit(id,Idprovider,contract,monto,iva)
{
    $('#txtEditContrato').val();
    $('#txtEditId').val();
    $('#txtEditContrato').val(contract);
    $('#txtEditId').val(id);
    $("#txtIdProviderEdit").val();
    $("#txtIdProviderEdit").val(Idprovider);
    $("#txtMontoEdit").val(0);
    $("#txtMontoEdit").val(monto);
    $("#txtIvaEdit").val(0);
    $("#txtIvaEdit").val(iva);
}
function search_provider_edit()
{
    $("#tbSearchEdit").show();
    $("#tbmodalbox").empty();
    $.ajax({
            type:'POST',
            url: '/contrato/edit/search/provider/',
            data:{
                    txtSearchProviderEdit:$("input[name=txtSearchProviderEdit]").val(),
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    },
            success:function(data)
            {
               $("#tbmodalbox").append(data);
            },
            error:function(req,e,er) {
                    msjError();
            }
            });
}
function setIdProviderEdit(id,name)
{
    $("#txtIdProviderEdit").val();
    $("#txtIdProviderEdit").val(id);
    $("#txtSearchProviderEdit").val(name);
    $("#tbSearchEdit").hide();

}
function save_edit()
{
    $.ajax({
            type:'POST',
            url: '/contrato/edit_save/',
            data:{
                    txtEditContrato:$("input[name=txtEditContrato]").val(),
                    txtIdProviderEdit:$("input[name=txtIdProviderEdit]").val(),
                    txtEditId:$("input[name=txtEditId]").val(),
                    txtMontoEdit:$("input[name=txtMontoEdit]").val(),
                    txtIvaEdit:$("input[name=txtIvaEdit]").val(),
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                    },
            success:function(data)
            {
               if (data >= 1)
                   {
                       msjSucces('Contrato modificado con exito !');
                       search_contract();
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

/*Here delete contract*/
function setDelete(idContrato,idProveedor)
{
    $('#txtIdContractDelete').val();
    $('#txtIdContractDelete').val(idContrato);
    $('#txtIdProviderDelete').val();
    $('#txtIdProviderDelete').val(idProveedor);
}
function delete_contract()
{
    $.ajax({
            type:'POST',
            url: '/contrato/delete/',
            data:{
                    txtIdContractDelete:$("input[name=txtIdContractDelete]").val(),
                    txtIdProviderDelete:$("input[name=txtIdProviderDelete]").val(),
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                    },
            success:function(data)
            {
               if (data >= 1)
                   {
                       msjSucces('El contrato fue eliminado !');
                       search_contract();
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

function iva_cal()
{
    var IVA = 0;
    IVA = $("#txtMonto").val() * $("#txtPIVA").val();
    $("#txtIVA").val(IVA);

}