/**
 * Server-to-client Messages handler
 * Tracks ?msg= in the url, parses it and display message(s)
 * ?msg=<message1Code>-<arg1>-<argN>,<message2Code>-<arg1>-<argN>
 * Arguments are optional and are used to replace '%n' tokens in the message strings
 * Message codes are used to resolve to message strings using the message map
 */

var messagesMap = {
	"userNotFound": "L'utilisateur %0 n'existe pas",
	"deleteOk": "Le cadeau a bien &eacute;t&eacute; effac&eacute;",
	"addOk": "Le cadeau a bien &eacute;t&eacute; ajout&eacute;",
	"searchedUserIsYou": "L'adresse email entr&eacute;e est la votre!",
	"missingSearchedEmail": "Veuillez entrer une adresse email pour ouvrir une liste",
	"needToBeLoggedToShare": "Vous devez vous connecter pour pouvoir partager votre liste",
	"needToBeLoggedToAdd": "Vous devez vous connecter pour pouvoir ajouter des cadeaux",
	"shareEmailSent": "Votre message a &eacute;t&eacute; envoy&eacute;",
	"incorrectSearchedEmail": "Veuillez entrer une adresse email correct pour ouvrir une liste"
};

function getRequestParams() {
	var url = $(location)[0].href;
	var paramStr = url.split("?")[1];
	if(paramStr) {
		var params = paramStr.split("&");
		var q = {};
		for(var p = 0; p < params.length; p ++){
			var kv = params[p].split("=");
			q[kv[0]] = kv[1];
		}

		return q;
	} else {
		return null;
	}
}

function displayMessages() {
	var params = getRequestParams();
	if(params && params.msg) {
		var messages = params.msg;
		if(messages) {
			messages = messages.split(",");
			var str = "<ul class='infoMessage'>";
			for(var m = 0; m < messages.length; m ++) {
				var msgParts = messages[m].split("-");
				var finalMsg = getFinalMessageString(msgParts[0], msgParts.splice(1));
				if(finalMsg) {
					str += "<li>" + finalMsg + "</li>";
				} else {
					continue;
				}
			}
			str += "</ul>";
			$('body').append(str);
			setTimeout(function(){$('.infoMessage').fadeOut(1500)}, 3000);
		}
	}
}

function getFinalMessageString(msgCode, params) {
	if(messagesMap[msgCode]) {
		var str = messagesMap[msgCode];
		if(params) {
			for(var p = 0; p < params.length; p ++) {
				str = str.replace("%" + p, params[p]);
			}
		}
		return str;
	} else {
		return null;
	}
}

displayMessages();