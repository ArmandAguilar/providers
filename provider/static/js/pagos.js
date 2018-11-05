$(document).ready(function() {

	// BOOTSTRAP DATEPICKER WITH AUTO CLOSE
    // =================================================================
    // Require Bootstrap Datepicker
    // http://eternicode.github.io/bootstrap-datepicker/
    // =================================================================
    $('#txtFechaPago').datepicker({
    autoclose:true,
    format: "yyyy-mm-dd"
    });
    $('#txtFechaPagoCal').datepicker({
    autoclose:true,
    format: "yyyy-mm-dd"
    });
    // SWITCHERY - SIZES
    // =================================================================
    // Require Switchery
    // http://abpetkov.github.io/switchery/
    // =================================================================
    //new Switchery(document.getElementById('demo-sw-sz-lg'), { size: 'large' });
    new Switchery(document.getElementById('demo-sw-unchecked'));
    new Switchery(document.getElementById('demo-sw-unchecked-nodo'));


});
function load()
{
    var simpleDate = new Date();
    var month = simpleDate.getMonth() + 1;
    var year = simpleDate.getFullYear();

    if ($("#CboMes option:selected").val() == 0)
     {

     }
     else{
            month = $("#CboMes option:selected").val();
     }
     if ($("input[name=txtYear]").val() == '')
     {

     }
     else{
            year = $("input[name=txtYear]").val();
     }
    $("#DashBoardContainer").empty();
     $.ajax({
                type:'POST',
                url: '/pagos/dashboard/',
                data:{
                        CboMes:month,
                        txtYear:year,
                        txtContable:$("#txtContable").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                   $("#DashBoardContainer").append(data);
                },
                error:function(req,e,er) {
                        msjError();
                }
              });
}
/*Here set Id for channge date */
function setIdForDate(id,date,trigger)
{
    $("#txtIdDate").val('');
    $("#txtIdDate").val(id);
    $("#txtFechaPago").val('');
    $("#txtFechaPago").val(date);
    $("#txtTrigger").val('');
    $("#txtTrigger").val(trigger);

}


function update_date_pay()
{
    $.ajax({
                type:'POST',
                url: '/pagos/update/fechapago/',
                data:{
                        txtIdDate:$("input[name=txtIdDate]").val(),
                        txtFechaPago:$("input[name=txtFechaPago]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                  if (data >= 1)
                     {
                        msjSucces('La fecha fue cambia con exito !');
                        if ($("#txtTrigger").val() > 0)
                           {
                                setTimeout(function(){ seek_providers(); }, 5000);
                                $("#txtTrigger").val('')
                           }
                         else{
                                setTimeout(function(){ load(); }, 5000);
                         }

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

function setIdForPayStatus(id,Factura,Importe,Iva,trigger)
{
    $("#txtIdBills").val('');
    $("#txtIdBills").val(id);
    $("#txtTrigger").val('');
    $("#txtTrigger").val(trigger);

    $("#txtFactura").val('');
    $("#txtFactura").val(Factura);

    $("#txtImporte").val('');
    $("#txtImporte").val(Importe);

    $("#txtIva").val('');
    $("#txtIva").val(Iva);
    load_bnk();
}

function load_bnk()
{
    $("#DivSelect").empty();
    $.ajax({
                type:'POST',
                url: '/pagos/update/loadBnk/',
                data:{
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                      },
                success:function(data)
                {
                    $("#DivSelect").append(data);
                    $("#DivSelect").addClass("selectpicker");
                },
                error:function(req,e,er) {
                        msjError();
                }
           });
}

function update_status_pay()
{
    $.ajax({
                type:'POST',
                url: '/pagos/update/status/',
                data:{
                        txtIdBills:$("input[name=txtIdBills]").val(),
                        txtFactura:$("input[name=txtFactura]").val(),
                        txtImporte:$("input[name=txtImporte]").val(),
                        txtIva:$("input[name=txtIva]").val(),
                        CboBnk:$("#CboBnk option:selected").val(),
                        txtuncontable:'Si',
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                  if (data >= 1)
                     {
                        msjSucces('El estado de la factura fue cambiado con exito !');
                        if ($("#txtTrigger").val() > 0)
                        {
                                setTimeout(function(){ seek_providers(); }, 5000);
                        }
                        else{
                                setTimeout(function(){ load(); }, 5000);
                        }

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
/*here code for cancel bills */
function setIdForCancel(id,trigger,amount,numProy)
{
    $("#txtIdCancel").val('');
    $("#txtIdCancel").val(id);
    $("#txtTrigger").val(trigger);

    $("#txtMonto").val('');
    $("#txtMonto").val(amount);

    $("#txtNumProy").val('');
    $("#txtNumProy").val(numProy);
}
function cancel_pay()
{
    $.ajax({
                type:'POST',
                url: '/pagos/cancel/bills/',
                data:{
                        txtIdCancel:$("input[name=txtIdCancel]").val(),
                        txtMonto:$("input[name=txtMonto]").val(),
                        txtNumProy:$("input[name=txtNumProy]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        txtuncontable:'Si',
                        },
                success:function(data)
                {
                  if (data >= 1)
                     {
                        msjSucces('Factura eliminada con exito !');
                        if ($("#txtTrigger").val() > 0)
                        {
                              setTimeout(function(){ load(); }, 5000);
                        }
                        else{
                              setTimeout(function(){ seek_providers(); }, 5000);
                        }
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
/* here code to edit bil*/
function link_go(url)
{
    window.location.href = url;
}
/* submenu to calendar or providers */
function cal()
{
    $("#DivProveedores").hide();
    $("#DivCalendario").show();

}
function providers()
{
    $("#DivCalendario").hide();
    $("#DivProveedores").show();
}
/*load tree providers*/
function load_tree_providers()
{
    $("#DivTbodyCon").empty();
        $.ajax({
                type:'POST',
                url: '/pagos/dashboard/tree/load/',
                data:{
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                      $("#DivTbodyCon").append(data);

                        $('#demo-foo-accordion').footable().on('footable_row_expanded', function(e) {
                            $('#demo-foo-accordion tbody tr.footable-detail-show').not(e.row).each(function() {
                                $('#demo-foo-accordion').data('footable').toggleDetail(this);
                            });
                        });


                        $('#demo-foo-pagination').footable();
                        $('#demo-show-entries').change(function (e) {
                            e.preventDefault();
                            var pageSize = $(this).val();
                            $('#demo-foo-pagination').data('page-size', pageSize);
                            $('#demo-foo-pagination').trigger('footable_initialized');
                        });
                },
                error:function(req,e,er) {
                        msjError();
                }
           });


}
/*here code to list providers */
function seek_providers()
{
    trigger = 0;
    if($('#txtProviders').val() == '')
    {
        if($('#txtFactura').val() == '')
        {
            if($('#txtProyecto').val() == '')
            {
                if($('#txtFechaPagoCal').val() == '')
                {
                     msjAlert(' todos los campos no pueden estar vacios');
                }
                else
                {
                    trigger = 1;
                }

            }
            else{
                    trigger = 1;
            }
        }
        else{
            trigger = 1;
        }
    }
    else{
        trigger = 1;
    }

    if (trigger > 0)
    {
        $("#DivTbodyCon").empty();
        $.ajax({
                type:'POST',
                url: '/pagos/dashboard/tree/',
                data:{
                        txtProviders:$("input[name=txtProviders]").val(),
                        txtFactura:$("input[name=txtFactura]").val(),
                        txtProyecto:$("input[name=txtProyecto]").val(),
                        txtFechaPago:$("input[name=txtFechaPagoCal]").val(),
                        txtContableNodo:$("input[name=txtContableNodo]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                      $("#DivTbodyCon").append(data);

                        $('#demo-foo-accordion').footable().on('footable_row_expanded', function(e) {
                            $('#demo-foo-accordion tbody tr.footable-detail-show').not(e.row).each(function() {
                                $('#demo-foo-accordion').data('footable').toggleDetail(this);
                            });
                        });


                        $('#demo-foo-pagination').footable();
                        $('#demo-show-entries').change(function (e) {
                            e.preventDefault();
                            var pageSize = $(this).val();
                            $('#demo-foo-pagination').data('page-size', pageSize);
                            $('#demo-foo-pagination').trigger('footable_initialized');
                        });
                },
                error:function(req,e,er) {
                        msjError();
                }
           });

    }
}
/*here update bnk for providers*/
function set_idProviders_bnk(id,banco,cuenta,clabe)
{
  /*here set the value*/
  $("#txtIdProviderBnk").val('');
  $("#txtIdProviderBnk").val(id);

  /*here get all data for the form*/
   $("#txtBanco").val('');
   $("#txtCuenta").val('');
   $("#txtClabe").val('');

   $("#txtBanco").val(banco);
   $("#txtCuenta").val(cuenta);
   $("#txtClabe").val(clabe);

}

function save_edit_banco()
{
    $.ajax({
                type:'POST',
                url: '/proveedor-projecto/save_edit_banco/',
                data:{
                        txtBanco:$("input[name=txtBanco]").val(),
                        txtCuenta:$("input[name=txtCuenta]").val(),
                        txtClabe:$("input[name=txtClabe]").val(),
                        txtIdProvider:$("input[name=txtIdProviderBnk]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                    if(data == 1)
                    {
                        msjSucces('Datos actualizados con exito !');
                        load();
                    }
                },
                error:function(req,e,er) {
                        msjError();
                }
                });

}
/*here set the value for contable or uncontable*/
function set_uncontable()
{
    $("#txtContable").val('No');
    if($("#demo-sw-unchecked").is(':checked')) {
            $("#txtContable").val('No');
    }
    else{
          $("#txtContable").val('Si');
    }
}

function set_uncontable_node()
{
    $("#txtContableNodo").val('Si');
    if($("#demo-sw-unchecked-nodo").is(':checked')) {
            $("#txtContableNodo").val('Si');
    }
    else{
          $("#txtContableNodo").val('No');
    }
}


function update_status_pay_uncontable()
{

    $.ajax({
                type:'POST',
                url: '/pagos/update/status/',
                data:{
                        txtIdBills:$("input[name=txtIdBillsUnContable]").val(),
                        txtFactura:$("input[name=txtFacturaUnContable]").val(),
                        txtImporte:$("input[name=txtImporteUnContable]").val(),
                        txtIva:$("input[name=txtIvaUnContable]").val(),
                        txtuncontable:'No',
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                  if (data >= 1)
                     {
                        msjSucces('El estado de la factura fue cambiado con exito !');
                        if ($("#txtTrigger").val() > 0)
                        {
                                setTimeout(function(){ seek_providers(); }, 5000);
                        }
                        else{
                                setTimeout(function(){ load(); }, 5000);
                        }

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
function setIdForPayStatus_uncontable(id,Factura,Importe,Iva,trigger)
{
    $("#txtIdBillsUnContable").val('');
    $("#txtIdBillsUnContable").val(id);
    $("#txtTrigger").val('');
    $("#txtTrigger").val(trigger);

    $("#txtFacturaUnContable").val('');
    $("#txtFacturaUnContable").val(Factura);

    $("#txtImporteUnContable").val('');
    $("#txtImporteUnContable").val(Importe);

    $("#txtIvaUnContable").val('');
    $("#txtIvaUnContable").val(Iva);

}

function setIdForCancel_uncontable(id,trigger,amount,numProy)
{
    $("#txtIdCancelUnContable").val('');
    $("#txtIdCancelUnContable").val(id);
    $("#txtTrigger").val(trigger);

    $("#txtMontoUnContable").val('');
    $("#txtMontoUnContable").val(amount);

    $("#txtNumProyUnContable").val('');
    $("#txtNumProyUnContable").val(numProy);
}
function cancel_pay_uncontable()
{
    $.ajax({
                type:'POST',
                url: '/pagos/cancel/bills/',
                data:{
                        txtIdCancel:$("input[name=txtIdCancelUnContable]").val(),
                        txtMonto:$("input[name=txtMontoUnContable]").val(),
                        txtNumProy:$("input[name=txtNumProyUnContable]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        txtuncontable:'No',
                        },
                success:function(data)
                {
                  if (data >= 1)
                     {
                        msjSucces('Factura eliminada con exito !');
                        if ($("#txtTrigger").val() > 0)
                        {
                              setTimeout(function(){ load(); }, 5000);
                        }
                        else{
                              setTimeout(function(){ seek_providers(); }, 5000);
                        }
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
/*here  for rewviews */
function set_valProveederReview(idProyecto,idProveedor){
        $("#IdProveedorReview").val('');
        $("#IdProyectoReview").val('');

        $("#IdProveedorReview").val(idProveedor);
        $("#IdProyectoReview").val(idProyecto);
}
function add_review()
{
    if($("#CboCalificacion option:selected").val() == 'NA')
    {
        msjAlert(' tienes que selecionar una calificacion');
    }
    else{
        if($("#CboCalidad option:selected").val() == 'NA')
        {
            msjAlert(' tienes que selecionar una calidad');
        }
        else{
            if($("#CboEntrega option:selected").val() == 'NA')
            {
                msjAlert(' tienes que selecionar una entrega de trabajo');
            }
            else{
                    $.ajax({
                        type:'POST',
                        url: '/pagos/review/add/',
                        data:{
                                CboCalificacion:$("#CboCalificacion option:selected").val(),
                                CboCalidad:$("#CboCalidad option:selected").val(),
                                CboEntrega:$("#CboEntrega option:selected").val(),
                                txtComentario:$("#txtComentario").val(),
                                IdProveedorReview:$("input[name=IdProveedorReview]").val(),
                                IdProyectoReview:$("input[name=IdProyectoReview]").val(),
                                IdUserReview:$("input[name=IdUserReview]").val(),
                                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                                txtuncontable:'No',
                                },
                        success:function(data)
                        {
                          if (data >= 1)
                             {
                                msjSucces(' Proveedor evaluado con exito');

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
        }
    }
}

load();