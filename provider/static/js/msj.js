function msjSucces(mjs)
{

    $.niftyNoty({
               type: 'success',
               icon : 'fa fa-check',
               message : mjs,
               container : 'floating',
               timer : 3000
            });
}

function msjAlert(msj)
{
        $.niftyNoty({
                		type: 'danger',
                		icon : 'fa fa-minus',
                		message : msj,
                		container : 'floating',
                		timer : 3000
                	});
}

function msjError()
{
        $.niftyNoty({
                		type: 'danger',
                		icon : 'fa fa-minus',
                		message : 'oh! a ocurrido un error.',
                		container : 'floating',
                		timer : 3000
                	});
}