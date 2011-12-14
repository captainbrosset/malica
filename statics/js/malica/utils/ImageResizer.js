if(!malica) {
	var malica = {};
}

/**
 * The ImageResizer takes in a list of images (jquery selected) and a max dimension
 * and resizes them if needed to the max dim
 * !! Images must be visibility hidden in the page for this to work
 */
malica.ImageResizer = function($images) {
	this._$images = $images;
};
/**
 * Will resize the set of images while they are loading by making sure they are really
 * done loading and then checking their sizes.
 * !! Images must be visibility hidden in the page for this to work
 */
malica.ImageResizer.prototype.resizeOnPageLoad = function(maxDim, noResizeIfSmaller) {
	this._$images.each(function() {
		var photo = this;
		var img = new Image();
		img.addEventListener('load', function() {
			if(photo.width < 50 && photo.height < 50) {
				photo.style.display = "none";
			} else if(photo.width > 1000 || photo.height > 1000) {
				photo.style.display = "none";
			} else {
				if(noResizeIfSmaller && photo.width < maxDim && photo.height < maxDim) {
					photo.style.visibility = "visible";
				} else {
					if(photo.width > photo.height) {
						photo.width = maxDim;
					} else {
						photo.height = maxDim;
					}
					photo.style.visibility = "visible";
				}
			}
		}, false);
		img.src = photo.src;
	});	
};