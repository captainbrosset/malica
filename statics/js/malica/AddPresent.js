if(!malica) {
	var malica = {};
}

malica.AddPresentPage = function($smartInput) {
	this._$smartInput = $smartInput;
};
malica.AddPresentPage.prototype.init = function() {
	var self = this;
	this._$smartInput.blur(function() {
		var parsedInput = malica.SmartInputDetector.detect(this.value);
		if(!parsedInput.url) {
			self._startSimpleAddition(parsedInput.description);
		} else {
			self._startUrlAddition(parsedInput.url, parsedInput.description);
		}
	});
};
malica.AddPresentPage.prototype._startSimpleAddition = function(description) {
	$("#title").val(description);
	// TODO: jsonp google image search API
};
malica.AddPresentPage.prototype._startUrlAddition = function(url, description) {
	$("#url").val(url);
	$("#title").val(description);
	
	$.getJSON("json_getInfoFromUrl?url=" + encodeURIComponent($("#url").val()), function(data) {
		var images = data.img;
		var title = data.title;
		var price = parseInt(data.price);
		
		$("#title").val(title);
		$("#approximatePrice").val(price);
		// FIXME: Beware of memory leaks ! Especially with the new event listener on image loading
		$("#images").html("");

		for(var i = 0, l = images.length; i < l; i ++) {
			$("#images").append("<li><img src='" + images[i] + "' style='visibility:hidden;' /></li>");
		}

		var resizer = new malica.ImageResizer($("#images img"));
		resizer.resizeOnPageLoad(150, true);

		$("#images img").bind("click", function() {
			$("#image").val(this.src);
			$("#images img").removeClass("selected");
			$(this).addClass("selected");
		});
	});
};
malica.AddPresentPage.prototype._ = function() {
	// Prevent submition of empty
	$('#addPresentForm').bind("submit", function(){
		if($("#url")[0].value == "") {
			$("#url").focus();
			return false;
		}
	});

	$("#simpleAddLink").bind("click", function(){
		$("#addPresentForm").addClass("hidden");
		$("#addSimplePresentForm").removeClass("hidden");
	});

	$("#webAddLink").bind("click", function(){
		$("#addPresentForm").removeClass("hidden");
		$("#addSimplePresentForm").addClass("hidden");
	});
	
	$("#url").blur(function() {

	});
};