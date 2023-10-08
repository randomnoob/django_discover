jQuery(function($) {
  "use strict";
	
	/* Loading Js*/
	function loader() {
		$(window).on('load', function () {
			$('#ctn-preloader').addClass('loaded');
			$("#loading").fadeOut(1000);
			// Una vez haya terminado el preloader aparezca el scroll

			if ($('#ctn-preloader').hasClass('loaded')) {
				// Es para que una vez que se haya ido el preloader se elimine toda la seccion preloader
				$('#preloader').delay(1400).queue(function () {
					$(this).remove();
				});
			}
		});
	}
	loader();

	/* Mobile Menu */
	jQuery(".nav.navbar-nav li a").on("click", function() { 
		jQuery(this).parent("li").find(".utf_dropdown_menu").slideToggle();
		jQuery(this).find("li i").toggleClass("fa-angle-down fa-angle-up");
	});

	$('.nav-tabs[data-toggle="tab-hover"] > li > a').hover( function(){
    	$(this).tab('show');
	});
	
	/* Site search */
	$('.utf_nav_search').on('click', function () {
		$('.utf_search_block').fadeIn(350);
    });

	$('.utf_search_close').on('click', function(){
		$('.utf_search_block').fadeOut(350);
	});

	$('.navbar-nav .menu-dropdown').on('click', function (event) {
		event.preventDefault();
		event.stopPropagation();
		$(this).siblings().slideToggle();
	});
	
	$('.nav-tabs[data-toggle="tab-hover"] > li > a').hover( function(){
    	$(this).tab('show');
	});

	/*Fixed Header **/
	$(window).on('scroll', function () {
		if ($(window).scrollTop() > 250) {
		   $('.utf_sticky').addClass('sticky fade_down_effect');
		} else {
		   $('.utf_sticky').removeClass('sticky fade_down_effect');
		}
	});	
	
	/* Back to top */
	$(window).scroll(function () {
		if ($(this).scrollTop() > 50) {
			 $('#back-to-top').fadeIn();
		} else {
			 $('#back-to-top').fadeOut();
		}
	});
	
	// scroll body to 0px on click
	$('#back-to-top').on('click', function () {
		 $('#back-to-top').tooltip('hide');
		 $('body,html').animate({
			  scrollTop: 0
		 }, 800);
		 return false;
	});
	$('#back-to-top').tooltip('hide');	
});