$(document).ready(function() {




// CIRCULAR FORM WIZARD
	// =================================================================

    $('#demo-step-wz').bootstrapWizard({
		tabClass		: 'wz-steps',
		nextSelector	: '.next',
		previousSelector	: '.previous',
		onTabClick: function(tab, navigation, index) {
			return false;
		},
		onInit : function(){
			$('#demo-step-wz').find('.finish').hide().prop('disabled', true);
		},
		onTabShow: function(tab, navigation, index) {
			var $total = navigation.find('li').length;
			var $current = index+1;
			var $percent = (index/$total) * 100;
			var wdt = 100/$total;
			var lft = wdt*index;
			var margin = (100/$total)/2;
			$('#demo-step-wz').find('.progress-bar').css({width:$percent+'%', 'margin': 0 + 'px ' + margin + '%'});


			// If it's the last tab then hide the last button and show the finish instead
			if($current >= $total) {
				$('#demo-step-wz').find('.next').hide();
				$('#demo-step-wz').find('.finish').show();
				$('#demo-step-wz').find('.finish').prop('disabled', false);
			} else {
				$('#demo-step-wz').find('.next').show();
				$('#demo-step-wz').find('.finish').hide().prop('disabled', true);
			}
		}
	});
	// BOOTSTRAP DATEPICKER WITH AUTO CLOSE
    // =================================================================
    // Require Bootstrap Datepicker
    // http://eternicode.github.io/bootstrap-datepicker/
    // =================================================================
    $('#txtFechaPago').datepicker({
    autoclose:true,
    format: "yyyy-mm-dd"
    });
    // SWITCHERY - SIZES
    // =================================================================
    // Require Switchery
    // http://abpetkov.github.io/switchery/
    // =================================================================
    //new Switchery(document.getElementById('demo-sw-sz-lg'), { size: 'large' });
    new Switchery(document.getElementById('demo-sw-sz'));
    new Switchery(document.getElementById('demo-sw-szPL'));
});

function search_provider()
{
        $("#tbSearch").empty();
        $("#DivContainer").show();
        $.ajax({
                type:'POST',
                url: '/proveedor-projecto/provider/search/',
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
/*Here set names and values for Id of provders*/
function set_Provider(id,name,banco,cuenta,clabe,tipo_persona)
{
    /* here val hidden */
    $("#txtIdProvider").val('');
    $("#txtIdProvider").val(id);
    /* here val in label */
    $("#lblProvider").empty();
    $("#lblProvider").append(name);
    /*here hide the search */
    $("#DivContainer").hide();
    /*here set in screen name provider step 3 */
    $("#lblProviderSel").empty();
    $("#lblProviderSel").append(name);

    /*for new contract*/
    $("#lblProviderForNewContract").empty();
    $("#lblProviderForNewContract").append(name);

    /*here show the bnk data*/
    $("#lblBanco").empty();
    $("#lblCuenta").empty();
    $("#lblClabe").empty();

    $("#lblBanco").append('Banco: ' + banco);
    $("#lblCuenta").append('Cuenta: ' + cuenta);
    $("#lblClabe").append('Clabe: ' + clabe);

    /*here set values in modal box*/
    $("#txtBanco").val('');
    $("#txtCuenta").val('');
    $("#txtClabe").val('');

    $("#txtBanco").val(banco);
    $("#txtCuenta").val(cuenta);
    $("#txtClabe").val(clabe);

    /*here set type of person */
    $("#txtTipoPersona").val(tipo_persona);
    /*here set the Retetion of tax*/
    if(tipo_persona == 'Fisica')
    {
        $("#DivISR").show();
        $("#DivISRIVA").show();
    }
    else{
        $("#DivISR").hide();
        $("#DivISRIVA").hide();
    }
    /*load all contract of provider sel */
    load_contract();

}
/*here make seek of proyescts */
function search_project()
{
        $("#tbSearchProjecto").empty();
        $("#DivContainerProyects").show();
        $.ajax({
                type:'POST',
                url: '/proveedor-projecto/project/search/',
                data:{
                        txtSearchProject:$("input[name=txtSearchProject]").val(),
                        txtAdmin:$("input[name=txtAdmin]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                   $("#tbSearchProjecto").append(data);
                },
                error:function(req,e,er) {
                        msjError();
                }
                });

}
/* here set values for the selection project*/
function set_Proyect(id,name)
{
 /* here val hidden */
    $("#txtIdProject").val('');
    $("#txtIdProject").val(id);
    /* here val in label */
    $("#lblProject").empty();
    $("#lblProject").append(name);
    /*here hide the search */
    $("#DivContainerProyects").hide();
    /*here set in screen name provider step 3 */
    $("#lblProySel").empty();
    $("#lblProySel").append(name);
}

/*here load cbo lider in form */
function load_leader()
{
        $.ajax({
                type:'POST',
                url: '/proveedor-projecto/cbo_lider/',
                data:{
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                        $("#CboLider").append(data);
                },
                error:function(req,e,er) {
                        msjError();
                }
                });
}

/*here load contract of the providers */
function load_contract()
{
        $("#CboContrato").empty();
        $.ajax({
                type:'POST',
                url: '/proveedor-projecto/cbo_contract/',
                data:{
                        txtIdProvider:$("input[name=txtIdProvider]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                       $("#CboContrato").append(data);
                },
                error:function(req,e,er) {
                        msjError();
                }
                });
}
/*here fucnton to make a new contract*/
function new_contract()
{
    if($("#txtContrato").val() == '')
        {
            msjAlert(' El campor contrato no pued estar vacio.');
        }
      else{
             if($("#txtIdProvider").val() == '')
             {
                msjAlert(' Debes de tener un proveedor selecionado.');
             }
             else{
                    $.ajax({
                            type:'POST',
                            url: '/contrato/save/',
                            data:{
                                    txtContrato:$("input[name=txtContrato]").val(),
                                    txtIdProveedor:$("input[name=txtIdProvider]").val(),
                                    txtMonto:$("input[name=txtMontoContrato]").val(),
                                    txtIVA:$("input[name=txtIVAContrato]").val(),
                                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                                    },
                            success:function(data)
                            {
                                   if (data >= 1)
                                   {
                                       msjSucces('Contrato asigando con exito !');
                                       load_contract();
                                       $("#txtContrato").val('');
                                       $("#txtMonto").val('');
                                       $("#txtIVA").val('');
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
/* here send data to make the union in the table */
function validate_data()
{
    if($("input[name=txtIdProvider]").val() == '')
    {
        msjAlert('Debes de selecionar un proveedor.');
    }
    else{
            if($("input[name=txtIdProject]").val() == '')
            {
                msjAlert('Debes de seleccionar un proyecto');
            }
            else{
                    if($("#CboContrato option:selected").val()== 0)
                    {
                        msjAlert('Debes de selecionar un contrato');
                    }
                    else{
                            if($("#CboLider option:selected").val() == 0)
                            {
                                msjAlert('Debes de selecionar un lider de proyecto');
                            }
                            else{
                                    if($("input[name=txtFactura]").val() == '')
                                    {
                                        msjAlert('Captura una Factura');
                                    }
                                    else{
                                        if($("input[name=txtMonto]").val() == '')
                                        {
                                            msjAlert('Camptura el monto de la factura');
                                        }
                                        else{
                                            if($("input[name=txtFechaPago]").val() == '')
                                            {
                                                msjAlert('Asigna una fecha de pago');
                                            }
                                            else{
                                                   if($("#txtConcepto").val() == '')
                                                   {
                                                        msjAlert('Escribe un concepto para esta factura');
                                                   }
                                                   else{
                                                        if($("#txtIva").val() == '')
                                                        {
                                                            msjAlert('El campo iva no puede estar vacio');
                                                        }
                                                        else{
                                                            save_data();
                                                        }

                                                   }
                                            }
                                        }
                                    }
                            }
                    }
            }
    }
}
function save_data()
{
    $.ajax({
                type:'POST',
                url: '/proveedor-projecto/save/',
                data:{
                        txtIdProvider:$("input[name=txtIdProvider]").val(),
                        txtIdProject:$("input[name=txtIdProject]").val(),
                        CboContrato:$("#CboContrato option:selected").val(),
                        CboLider:$("#CboLider option:selected").val(),
                        txtFactura:$("input[name=txtFactura]").val(),
                        txtMonto:$("input[name=txtMonto]").val(),
                        txtFechaPago:$("input[name=txtFechaPago]").val(),
                        txtConcepto:$("#txtConcepto").val(),
                        txtIva:$("input[name=txtIva]").val(),
                        txtContable:$("input[name=txtContable]").val(),
                        txtReferencia:$("input[name=txtReferencia]").val(),
                        txtISR:$("input[name=txtISR]").val(),
                        txtISRIVA:$("input[name=txtISRIVA]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                   if (data == 1)
                   {
                        msjSucces('Factura registrado con exito !');
                        setTimeout(function(){ window.location.href='/proveedor-projecto/';}, 5000);
                   }
                   else{
                        if(data == 2)
                        {
                            msjAlert("Error: El total de facturas excede el monto del contrato.")
                        }
                        else{
                             msjError();
                        }

                   }
                },
                error:function(req,e,er) {
                        msjError();
                }
                });
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
                        txtIdProvider:$("input[name=txtIdProvider]").val(),
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {
                    if(data == 1)
                    {
                        msjSucces('Datos actualizados con exito !');
                    }
                },
                error:function(req,e,er) {
                        msjError();
                }
                });

}
/*here set the value when the user haven't bills*/
function set_bills()
{
    $("#txtFactura").val('');
    $("#txtFactura").val('Provisionar');
}
/*here set the value for contable or uncontable*/
function set_uncontable()
{
    $("#txtContable").val('Si');
    if($("#demo-sw-sz").is(':checked')) {
            $("#txtContable").val('Si');
    }
    else{
          $("#txtContable").val('No');
    }
}
/*here set the value for Produccion or Local*/
function set_ProyLocal()
{
    $("#txtAdmin").val('Si');
    if($("#demo-sw-szPL").is(':checked')) {
            $("#txtAdmin").val('Si');
            //$("#txtContable").val('No');
            //$("#DivUnContable").hide();
    }
    else{
          $("#txtAdmin").val('No');
          //$("#DivUnContable").show();
    }
}
/*Calculo de iva */
function calculo_iva_fact()
{
    var monto = $("#txtMonto").val();
    var Iva = 0;
    Iva = monto * $("#txtPIva").val();
    $("#txtIva").val(Iva);
}
function calculo_contrato_iva()
{
    var monto = $("#txtMontoContrato").val();
    var Iva = 0;
    Iva = monto * $("#txtPIVAContrato").val();
    $("#txtIVAContrato").val(Iva);
}

function calcular_isr()
{
    IvaISR = $("#txtISR").val() * $("#txtPIva").val();
    $("#txtISRIVA").val(IvaISR);
}




