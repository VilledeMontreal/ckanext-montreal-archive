$(function(){
	// Pour afficher les option de recherche CKAN vs Wordpress
	$( "#afficher-options-de-recherche" ).click(function() {
		$( "#bloc-recherche-permament" ).slideToggle('fast');
	});
	// Pour afficher les option de recherche CKAN vs Wordpress sur la page d'accueil
	$( "body.home #afficher-options-de-recherche" ).click(function() {
		$( "#commutateur-recherche" ).toggle();	
	});
	$( "body.home #expression-de-recherche" ).focus(function() {
		$( "#commutateur-recherche" ).show();	
	});
	// Pour modifier le formulaire de recherche dynamiquement:
	$( "#recherche-ckan" ).click(function() {
		$( "#formulaire-de-recherche" ).attr("action","http://donnees.ville.montreal.qc.ca/dataset");
		$( "#expression-de-recherche" ).attr("name","q");
		$( "#expression-de-recherche" ).attr("placeholder", "Rechercher un ensemble de données");
		//alert( "Dans CKAN" );			
	});
	$( "#recherche-wordpress" ).click(function() {	
		$( "#formulaire-de-recherche" ).attr("action","/");		
		$( "#expression-de-recherche" ).attr("name","s");
		$( "#expression-de-recherche" ).attr("placeholder", "Rechercher parmi les actualités, applications et pages d'aide");
		//alert( "Dans Wordpress" );
	});	
});