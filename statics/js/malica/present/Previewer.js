if(!malica) {
	var malica = {};
}
if(!malica.present) {
	malica.present = {};
}

/**
 * The previewer class can be used with a presentItem HTML structure to preview a present before adding it to the list.
 * It just exposes a set of methods that are used to display a url, description, price and image
 */
malica.present.Previewer = function($el) {
	/**
	 * The presentItem HTML element
	 * @type jQuery
	 * @private
	 */
	this._$presentPreviewEl = $el;
};

malica.present.Previewer.prototype.IMG_MAX_DIM = 200;

/**
 * Reset all of the present attributes
 */
malica.present.Previewer.prototype.reset = function(image) {
	this.setDescription();
	this.setPrice("--");
	this.setUrl();
	this.setImage();
};

/**
 * Set the image of a present to be previewed
 */
malica.present.Previewer.prototype.setImage = function(image) {
	if(!image) {
		$(".img", this._$presentPreviewEl).html("&nbsp;<img src='/statics/images/noImage.png' /> ");
	} else {
		var resizer = new Image(), imgSizeAttribute = "";
		resizer.src = image.src;
		var isBiggerThanMaxSize = resizer.width > this.IMG_MAX_DIM || resizer.height > this.IMG_MAX_DIM;

		if(isBiggerThanMaxSize) {
			if(resizer.width > resizer.height) {
				imgSizeAttribute = " width='" + this.IMG_MAX_DIM + "'";
			} else {
				imgSizeAttribute = " height='" + this.IMG_MAX_DIM + "'";
			}
		}
	
		$(".img", this._$presentPreviewEl).html("&nbsp;<img src='" + image.src + "'" + imgSizeAttribute + " /> ");
	}
};

/**
 * Set the description of a present to be previewed
 */
malica.present.Previewer.prototype.setDescription = function(description) {
	$(".title", this._$presentPreviewEl).html(description);
};

/**
 * Set the price of a present to be previewed
 */
malica.present.Previewer.prototype.setPrice = function(price) {
	$(".price span", this._$presentPreviewEl).html(price);
};

/**
 * Set the url of a present to be previewed
 */
malica.present.Previewer.prototype.setUrl = function(url) {
	if(url) {
		var indexOfSlashAfterDomain = url.indexOf("/", 8), isLongUrl = indexOfSlashAfterDomain != -1, shortUrl = url;
		if(isLongUrl) {
			shortUrl = url.substring(0, indexOfSlashAfterDomain);
		}
		$(".url", this._$presentPreviewEl).html("<a href='" + url + "' target='new'> &raquo; " + shortUrl + "</a>");
	} else {
		$(".url", this._$presentPreviewEl).html("");
	}
};