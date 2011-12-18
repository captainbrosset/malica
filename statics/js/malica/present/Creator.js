if(!malica) {
	var malica = {};
}
if(!malica.present) {
	malica.present = {};
}

malica.present.Creator = function() {
	this._$smartInput = $('#smartInput');
	this._previewer = new malica.present.Previewer($("#addPresentPreview"));
	this._step = 1;
};
malica.present.Creator.prototype.init = function() {
	var self = this;
	this._$smartInput.blur(function() {
		self.firstStep();
		self._previewer.reset();
		$("#images").html("");
		var parsedInput = malica.SmartInputDetector.detect(this.value);
		if(!parsedInput.url) {
			self._startSimpleAddition(parsedInput.description);
		} else {
			$("#url").val(parsedInput.url);
			self._startUrlAddition(parsedInput.url, parsedInput.description);
		}
	});
	this._$smartInput.focus();
	$("button").click(function() {
		self.nextStep();
		return false;
	});
	$("#title").blur(function() {
		if($(this).val()) {
			self._previewer.setDescription($(this).val());
		}
	});
	$("#price").blur(function() {
		if($(this).val()) {
			self._previewer.setPrice($(this).val());
		}
	});
};
malica.present.Creator.prototype.firstStep = function() {
	$(".step[step]").hide();
	this._step = 1;
	this.startLoadingIndicatorOnImages();
};
malica.present.Creator.prototype.nextStep = function() {
	if(this._step == 5) {
		this.lastStep();
	} else {
		$(".step[step]").hide();	
		$(".step[step='" + this._step + "']").show();
		this._step ++;
	}
};
malica.present.Creator.prototype.lastStep = function() {
	// Submit the form to add the present! Everything is fine now
	$("form").submit();
};
malica.present.Creator.prototype.startLoadingIndicatorOnImages = function() {
	$("#images").addClass("loading");
};
malica.present.Creator.prototype.stopLoadingIndicatorOnImages = function() {
	$("#images").removeClass("loading");	
};
malica.present.Creator.prototype._startSimpleAddition = function(description) {
	this._previewer.setDescription(description);
	$("#title").val(description);
	var self = this;
	$.getJSON("https://ajax.googleapis.com/ajax/services/search/images?v=1.0&callback=?&q=" + encodeURIComponent(description), function(data) {
		if(data.responseData.results) {
			var images = [];
			for(var i = 0; i < data.responseData.results.length; i++) {
				images.push(data.responseData.results[i].unescapedUrl);
			}
			self._displayImages(images);
		}
	});
};
malica.present.Creator.prototype._startUrlAddition = function(url, description) {
	this._previewer.setUrl(url);
	this._previewer.setDescription(description);
	$("#title").val(description);
	var self = this;
	$.getJSON("json_getInfoFromUrl?url=" + encodeURIComponent(url), function(data) {
		var images = data.img;
		var description = data.title;
		var price = parseInt(data.price);
		
		self._previewer.setPrice(price);
		self._previewer.setDescription(description);
		$("#price").val(price);
		$("#title").val(description);
		
		self._displayImages(images);
	});
};
malica.present.Creator.prototype._displayImages = function(images) {
	this.stopLoadingIndicatorOnImages();
	
	for(var i = 0, l = images.length; i < l; i ++) {
		$("#images").append("<li><img src='" + images[i] + "' style='visibility:hidden;' /></li>");
	}
	// Always append the "no image" at the end as well
	$("#images").append("<li><img src='/statics/images/noImage.png' style='visibility:hidden;' /></li>");

	var resizer = new malica.ImageResizer($("#images img"));
	resizer.resizeOnPageLoad(200, true);

	var self = this;
	$("#images img").bind("click", function() {
		$("#images img").removeClass("selected");
		$(this).addClass("selected");
		$("#photo").val(this.src);
		self._previewer.setImage(this);
	});	
};