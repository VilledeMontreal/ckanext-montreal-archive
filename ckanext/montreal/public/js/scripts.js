// JavaScript Document
var $j = jQuery.noConflict();

$j(function(){
	// Pour le menu sur mobiles
	$j('#nav li.menu-item-has-children').doubleTapToGo();
	$j('#menu-toggle').click(function() {
		$j('#site-navigation ul.nav-menu').slideToggle('fast');
	});
	// Ne sert qu'en page d'accueil!
	$j('#liste-categories li img').hover(function() {
		$j('#titre-groupe p').text($j(this).attr('alt'))
		$j('#titre-groupe p').show();
	});
	$j('#liste-categories li img').mouseout(function() {
		$j('#titre-groupe p').hide();
	});
	// Pour afficher les option de recherche CKAN vs Wordpress
	$j('#afficher-options-de-recherche').click(function() {
		$j('#bloc-recherche-permament').slideToggle('fast');
	});
	// Pour afficher les option de recherche CKAN vs Wordpress sur la page d'accueil
	$j('body.home #afficher-options-de-recherche').click(function() {
		$j('#commutateur-recherche').toggle();
	});
	$j('body.home #expression-de-recherche').focus(function() {
		$j('#commutateur-recherche').show();
	});
	// Pour modifier le formulaire de recherche dynamiquement:
	$j('#recherche-ckan').click(function() {
		$j('#formulaire-de-recherche').attr('action','http://donnees.ville.montreal.qc.ca/dataset');
		$j('#expression-de-recherche').attr('name','q');
		$j('#expression-de-recherche').attr('placeholder','Rechercher un ensemble de donnÃ©es');
		//alert('Dans CKAN');
	});
	$j('#recherche-wordpress').click(function() {
		$j('#formulaire-de-recherche').attr('action','/');
		$j('#expression-de-recherche').attr('name','s');
		$j('#expression-de-recherche').attr('placeholder',"Rechercher parmi les actualitÃ©s, applications et pages d'aide");
		//alert('Dans Wordpress');
	});
	// Pour masquer une partie du fil d'Ariane permettant de naviguer parmi les organisations (il n'y en a qu'une: la Ville!)
	if($j('div#content.container .toolbar ol li a[href="/organization"]').length) {
		$j('div#content.container .toolbar ol li a[href*="/organization"]').parent().remove();
		$j('div#content.container .toolbar ol li.home').after('<li><a href="/dataset">&nbsp;Ensembles de donnÃ©es</a></li>');
	};
	// Pour...
	if($j('div#content.container ul.activity p span.actor').length) {
		$j('div#content.container ul.activity p span.actor a').contents().unwrap();
	};
	// Patch pour la liste des territoires
	// html.js body.ckan div div#content.container div.row.wrapper div.primary.span9 article.module div.module-content section#territoires ul.tag-list.well
	if($j('section#territoires ul.tag-list.well').length) {
		//$j('section#territoires ul.tag-list.well ul').unwrap();
	};
	if($j('html').hasClass('ie ie7') || $j('html').hasClass('ie ie8')){
		if($j('.secondary.span3').parent().hasClass('primary span9')){
			var _html = $j('.secondary.span3');
			_html.insertAfter($j('.primary.span9'));
		}
	}
	/*patch pour faire disparaÃ®tre l'icon linkedin, voir ckan.css ligne:1069*/
	var moduleSocialIcons = $('.module-narrow.social ul.nav.nav-simple li.nav-item a i');
	$.each(moduleSocialIcons, function(){
		if(!$(this).hasClass('icon-linkedin-sign')){
			$(this).parents('li').css({
				'display':'block'
			});
		}
	});
})
