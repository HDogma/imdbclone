$(document).ready(function() {	
	$('#sponsorCarousel').owlCarousel({
		loop:true,
		margin:10,
		nav: true,
		autoplay: true,
		autoplayTimeout:5000,
		autoplayHoverPause:false,
		responsive:{
			0:{
				items:2
			},
			600:{
				items:4
			},
			1000:{
				items:5
			}
		}
	}); 


	var sponserNav = $('#sponsorCarousel .owl-nav > div');
	$(sponserNav).first().html('<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>');
	$(sponserNav).last().html('<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>');

	$('#sponsorCarousel .owl-dots').remove();
});