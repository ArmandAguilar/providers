$(document).ready(function() {

// CIRCULAR FORM WIZARD
	// =================================================================
	$('#demo-cir-wz').bootstrapWizard({
		tabClass		: 'wz-steps',
		nextSelector	: '.next',
		previousSelector	: '.previous',
		onTabClick: function(tab, navigation, index) {
		return false;
		},
		onInit : function(){
		$('#demo-cir-wz').find('.finish').hide().prop('disabled', true);
		},
		onTabShow: function(tab, navigation, index) {
		var $total = navigation.find('li').length;
		var $current = index+1;
		var $percent = (index/$total) * 100;
		var margin = (100/$total)/2;
		$('#demo-cir-wz').find('.progress-bar').css({width:$percent+'%', 'margin': 0 + 'px ' + margin + '%'});

		navigation.find('li:eq('+index+') a').trigger('focus');


		// If it's the last tab then hide the last button and show the finish instead
		if($current >= $total) {
			$('#demo-cir-wz').find('.next').hide();
			$('#demo-cir-wz').find('.finish').show();
			$('#demo-cir-wz').find('.finish').prop('disabled', false);
		} else {
			$('#demo-cir-wz').find('.next').show();
			$('#demo-cir-wz').find('.finish').hide().prop('disabled', true);
		}
		}
	})

	$('#demo-cir-wz-Factura-Proveedores').bootstrapWizard({
		tabClass		: 'wz-steps',
		nextSelector	: '.next',
		previousSelector	: '.previous',
		onTabClick: function(tab, navigation, index) {
		return false;
		},
		onInit : function(){
		$('#demo-cir-wz-Factura-Proveedores').find('.finish').hide().prop('disabled', true);
		},
		onTabShow: function(tab, navigation, index) {
		var $total = navigation.find('li').length;
		var $current = index+1;
		var $percent = (index/$total) * 100;
		var margin = (100/$total)/2;
		$('#demo-cir-wz-Factura-Proveedores').find('.progress-bar').css({width:$percent+'%', 'margin': 0 + 'px ' + margin + '%'});

		navigation.find('li:eq('+index+') a').trigger('focus');


		// If it's the last tab then hide the last button and show the finish instead
		if($current >= $total) {
			$('#demo-cir-wz-Factura-Proveedores').find('.next').hide();
			$('#demo-cir-wz-Factura-Proveedores').find('.finish').show();
			$('#demo-cir-wz-Factura-Proveedores').find('.finish').prop('disabled', false);
		} else {
			$('#ddemo-cir-wz-Factura-Proveedores').find('.next').show();
			$('#demo-cir-wz-Factura-Proveedores').find('.finish').hide().prop('disabled', true);
		}
		}
	})
});
