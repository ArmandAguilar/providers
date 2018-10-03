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
function set_Provider(id,name)
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
    /*Update contrato cbo*/
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
/*here load contract of the providers */
function load_contract(idProvider,IdContract)
{
        $("#CboContrato").empty();
        $.ajax({
                type:'POST',
                url: '/pagos/contract/',
                data:{
                        txtIdProvider:idProvider,
                        txtIdContract:IdContract,
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
/*load proyecto for edit */
function load_proyect_label(noProy)
{
            $("#lblProject").empty();
            $("#lblProySel").empty();
            $.ajax({
                type:'POST',
                url: '/pagos/noproy/',
                data:{
                        txtNoProy:noProy,
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                        },
                success:function(data)
                {

                       $("#lblProject").append(data);
                       $("#lblProySel").append(data);
                },
                error:function(req,e,er) {
                        msjError();
                }
                });
}
/* Here load Lider */
function load_leader_cbo(idLeader)
{
    $.ajax({
                type:'POST',
                url: '/pagos/leader/',
                data:{
                        txtidLeader:idLeader,
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
/*here edit and saves data*/
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
function save_data()
{
    $.ajax({
            type:'POST',
            url: '/pagos/bills/save_edit/',
            data:{
                    txtId:$("input[name=txtId]").val(),
                    txtIdProvider:$("input[name=txtIdProvider]").val(),
                    txtIdProject:$("input[name=txtIdProject]").val(),
                    CboContrato:$("#CboContrato option:selected").val(),
                    CboLider:$("#CboLider option:selected").val(),
                    txtFactura:$("input[name=txtFactura]").val(),
                    txtMonto:$("input[name=txtMonto]").val(),
                    txtIva:$("input[name=txtIva]").val(),
                    txtFechaPago:$("input[name=txtFechaPago]").val(),
                    txtConcepto:$("#txtConcepto").val(),
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    },
            success:function(data)
            {

               if (data >= 1)
               {
                    msjSucces('Factura cambiado con exito !');
                    setTimeout(function(){ window.location.href='/pagos/';}, 6000);
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
                                    txtIVA:$("input[name=txtIVA]").val(),
                                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                                    },
                            success:function(data)
                            {
                                   if (data >= 1)
                                   {
                                       msjSucces('Contrato asigando con exito !');
                                       load_contract($("#txtIdProvider").val(),$("#txtIdContrato").val());
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

/*here set the value when the user haven't bills*/
function set_bills()
{
    $("#txtFactura").val('');
    $("#txtFactura").val('Provisionar');
}
