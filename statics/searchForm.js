(function(){
	var helptext = "Ouvrir une liste existante. Entrer l’adresse email...";
	var input = $("#searchForm input");
	input.val(helptext);
	input.focus(function(){
		if(input.val() == helptext) {
			input.val("");
		}
	});
	input.blur(function(){
		if(input.val() == "") {
			input.val(helptext);
		}
	});
})();